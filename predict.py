import torch
import matplotlib.pyplot as plt
import cv2
import pandas as pd

y_pred
df
PATH = "C://Users//AEZ//Documents//SDI//RoadCracks//CFExp//weights.pt"
model = createDeepLabv3()
model = torch.load(PATH)
model.eval()


def load_model(model, model_path):
    model = model = torch.load(PATH)
    model.eval()
    return model

def load_single_image(ino):
    # Read  a sample image and mask from the data-set
    img = cv2.imread(f'./CrackForest/Images/{ino:03d}.jpg').transpose(2,0,1).reshape(1,3,320,480)
    mask = cv2.imread(f'./CrackForest/Masks/{ino:03d}_label.PNG')
    dtype = torch.cuda.float if torch.cuda.is_available() else torch.float
    with torch.no_grad():
        y_pred = model(torch.from_numpy(img).type(dtype)/255)

def plot_best_threshold(y_pred):
    # Plot histogram of the prediction to find a suitable threshold. From the histogram a 0.1 looks like a good choice.
    plt.hist(a['out'].data.cpu().numpy().flatten())

def plot_metrics_dict():
    # Read the log file using pandas into a dataframe
    df = pd.read_csv('./CFExp/log.csv')
    # Plot all the values with respect to the epochs
    df.plot(x='epoch',figsize=(15,8))

def plot_best_metric():
    print(df[['Train_auroc','Test_auroc']].max())

def plot_prediction():
    # Plot the input image, ground truth and the predicted output
    plt.figure(figsize=(10,10));
    plt.subplot(131);
    plt.imshow(img[0,...].transpose(1,2,0));
    plt.title('Image')
    plt.axis('off');
    plt.subplot(132);
    plt.imshow(mask);
    plt.title('Ground Truth')
    plt.axis('off');
    plt.subplot(133);
    plt.imshow(a['out'].cpu().detach().numpy()[0][0]> 0.2);
    plt.title('Segmentation Output')
    plt.axis('off');
    plt.savefig('./CFExp/SegmentationOutput.png',bbox_inches='tight')
