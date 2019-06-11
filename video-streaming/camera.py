import cv2
#import sys
#sys.path.append('/Users/hannah/Desktop/AS/tf-pose-estimation')
import tf_pose
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    # def get_frame(self):
    #     return ebi()
    # def ebi_icon(self):
    #     icon = cv2.imread("./icon/ebi.png")
    #     ret, jpeg = cv2.imencode('.jpg', icon)
    #     return jpeg.tobytes()
    def get_frame(self,pic):
        success, image = self.video.read()
        if pic == 'non':
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()
        # pose detection
        w, h = model_wh('0x0')
        e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(432, 368))
        humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=4.0)
        image_h, image_w = image.shape[:2]
        print('pic',pic)
        ebi=cv2.imread('./static/icon/'+pic+'.png')
        # ebi=cv2.imread('./static/icon/ebi.png')

        ebi_h, ebi_w = ebi.shape[:2]
        for human in humans:
            if 0 not in human.body_parts.keys():
                continue
            body_part = human.body_parts[0]
            center_1=int(body_part.x * image_w + 0.5)-ebi_w/2
            center_2=int(body_part.y * image_h + 0.5)-ebi_h/2
            for i in range (0,ebi_h):
                for j in range (0,ebi_w):
                    if ebi[i][j][0]!=0 or ebi[i][j][1]!=0 or ebi[i][j][2]!=0:
                        xx=int(center_2+i)
                        yy=int(center_1+j)
                        if xx>=0 and xx<image_h and yy>=0 and yy<image_w :
                            image[xx][yy]=ebi[i][j]


        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()