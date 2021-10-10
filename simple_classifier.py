import numpy as np
from cgrongenome import adjust
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler    
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report


def binary_acc(y_pred, y_test):
    y_pred_tag = torch.round(torch.sigmoid(y_pred))

    correct_results_sum = (y_pred_tag == y_test).sum().float()
    acc = correct_results_sum/y_test.shape[0]
    # print("ttaccuracy;", acc, correct_results_sum, y_test.shape[0])
    acc = torch.round(acc * 100)
    
    return acc

class trainData(Dataset):
	def __init__(self, X_data, y_data):
		self.X_data = X_data
		self.y_data = y_data

	def __getitem__(self, index):
		return self.X_data[index], self.y_data[index]

	def __len__ (self):
		return len(self.X_data)



class testData(Dataset):
	def __init__(self, X_data):
		self.X_data = X_data

	def __getitem__(self, index):
		return self.X_data[index]

	def __len__ (self):
		return len(self.X_data)



def dist_avg(seq):
	return (1 + asia)%2 if np.sum(np.abs(seq-avg_euro)) < np.sum(np.abs(seq-avg_asia)) else (asia)%2


def avg_classifier():
	global asia
	asia_acc = np.sum(list(map(dist_avg, asia_samples)))
	asia = False
	euro_acc = np.sum(list(map(dist_avg, euro_samples)))
	print("asia=", str(asia_acc/len(asia_samples)) + " euro=", str(euro_acc/len(euro_samples)) + " whole=",
	 str((asia_acc+euro_acc)/(len(asia_samples)+len(euro_samples))))


class binary_classifier(nn.Module):
	def __init__(self):
		super(binary_classifier, self).__init__()
		self.layer_1 = nn.Linear(1024, 500) 
		self.layer_2 = nn.Linear(500, 500)
		self.layer_out = nn.Linear(500, 1) 

		self.relu = nn.ReLU()
		self.dropout = nn.Dropout(p=0.1)
		self.batchnorm1 = nn.BatchNorm1d(500)
		self.batchnorm2 = nn.BatchNorm1d(500)


	def forward(self, inputs):
		x = self.relu(self.layer_1(inputs))
		x = self.batchnorm1(x)
		x = self.relu(self.layer_2(x))
		x = self.batchnorm2(x)
		x = self.dropout(x)
		x = self.layer_out(x)

		return x


def classify_torch():
	device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
	print(device)

	model = binary_classifier()
	model.to(device)
	print(model)
	criterion = nn.BCEWithLogitsLoss()
	optimizer = optim.Adam(model.parameters(), lr=0.001)


	# new_sampes = np.array(map(flatten, asia_samples))
	shape_two = asia_samples.shape[1] * asia_samples.shape[2]
	new_asia = asia_samples.reshape((asia_samples.shape[0], shape_two))

	new_euro = euro_samples.reshape((euro_samples.shape[0], shape_two))
	print(new_asia.shape, new_euro.shape)


	X = np.append(new_asia, new_euro, axis=0)
	X = X.astype(float)
	y = np.array([1.0]*asia_samples.shape[0] + [0.0]*euro_samples.shape[0])
	print(X.shape, len(y), np.sum(y))

	X, y = torch.from_numpy(X), torch.from_numpy(y)
	train_data = torch.utils.data.TensorDataset(X, y)

	scaler = StandardScaler()
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
	X_train = scaler.fit_transform(X_train)
	X_test = scaler.transform(X_test)

	# y= torch.FloatTensor(y_train)
	train_data = trainData(torch.FloatTensor(X_train), torch.DoubleTensor(y_train))
	test_data = testData(torch.FloatTensor(X_test))
	train_loader = DataLoader(dataset=train_data, batch_size=64, shuffle=True)
	test_loader = DataLoader(dataset=test_data, batch_size=1)


	model.train()
	for e in range(1, 51):
		epoch_loss = 0
		epoch_acc = 0
		for X_batch, y_batch in train_loader:
			X_batch, y_batch = X_batch.to(device), y_batch.to(device)
			optimizer.zero_grad()

			y_pred = model(X_batch)

			loss = criterion(y_pred, y_batch.unsqueeze(1))
			acc = binary_acc(y_pred, y_batch.unsqueeze(1))

			loss.backward()
			optimizer.step()

			epoch_loss += loss.item()
			epoch_acc += acc.item()


		print(f'Epoch {e+0:03}: | Loss: {epoch_loss/len(train_loader):.5f} | Acc: {epoch_acc/len(train_loader):.3f}')

	y_pred_list = []
	model.eval()
	with torch.no_grad():
		for X_batch in test_loader:
			X_batch = X_batch.to(device)
			y_test_pred = model(X_batch)
			y_test_pred = torch.sigmoid(y_test_pred)
			y_pred_tag = torch.round(y_test_pred)
			y_pred_list.append(y_pred_tag.cpu().numpy())


	y_pred = model(torch.FloatTensor(X_test))
	y_pred = torch.round(torch.sigmoid(y_pred))
	y_pred = torch.reshape(y_pred, (202,))
	
	print("final accuracy:", float((y_pred==y_test).sum().float()/y_pred.shape[0])*100, "%")

	y_pred_list = [a.squeeze().tolist() for a in y_pred_list]

	print("accuracy:", binary_acc(y_pred, y_test))
	print(classification_report(y_test, y_pred_list))

	

		

	# X_train, X_test, y_train, y_test = 

	# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=69)






if __name__ == "__main__":
	name_asia, name_euro = 'AsianCGR', 'EuroCGR'
	temp_load = 'avgfinal'
	asia = True

	avg_asia = np.load(temp_load + name_asia + '.npy')
	avg_euro = np.load(temp_load + name_euro +'.npy')
	print(avg_asia.shape)

	avg_base = np.load('chaos.out.npy')

	temp_load = 'cgrfinal_'
	asia_samples = np.load(temp_load+name_asia+'.npy')
	euro_samples = np.load(temp_load+name_euro+'.npy')
	
	# print(adjust)

	# avg_classifier()
	classify_torch()


