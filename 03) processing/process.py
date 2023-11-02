
import os
import pandas as pd
from CustomEnum import Details
from CustomTime import Time
from queue import Queue
import numpy
import cv2
import tensorflow as tf
import threading
from Thread_basics.cls_Producer import Producer
from Thread_basics.cls_Consumer import Cosnumer
from Thread_basics.cls_Readucer import Readucer
import concurrent.futures

class VideoProducer (threading.Thread,Producer):
    def __init__(self,q,dependicesQ,videoPath,modelPath,classes,shape):
        try:
            super().__init__()
            self.queue=q
            self.videoCapture=cv2.VideoCapture(videoPath)
            self.model=tf.keras.models.load_model(modelPath)
            self.dependicesQ=dependicesQ
            self.classes=classes
            self.shape=shape

            
            self.dependicesQ.put(self.model) #put the model
            self.dependicesQ.put(self.shape) #put the shape
            self.dependicesQ.put(self.classes) #put the classes

        except Exception as ex:
            print(str(ex))
            


    #@Override Method from abstract class
    def produce(self,q,videoStream):
        try:
           
            count=1
            while (True):
                ret, frame = videoStream.read()

                if not ret:
                    break

                if count %15==0:
                    frameTime = videoStream.get(cv2.CAP_PROP_POS_MSEC)
                    q.put((frameTime,frame))
                      
                count+=1  
                

            videoStream.release()
            cv2.destroyAllWindows()
            print("finish sending all the frames")
            q.put(None)
            q.put(None)
            q.put(None)
        except Exception as ex:
            print(str(ex))
        

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(self.produce, self.queue, self.videoCapture)
        
        
 

class Consumer(threading.Thread,Cosnumer):
    def __init__(self,q,dependcisQ,excelQueue):
        super().__init__()
        self.queue=q
        self.dependcisQ=dependcisQ
        self.excelQueue=excelQueue

        self.model=self.dependcisQ.get() #the first get will return model
        self.shape=self.dependcisQ.get() #the second get will return the shape
        self.classes=self.dependcisQ.get() #the third get will return the classes
       
    #@Override Method from abstract class
    def consume(self,q,model,classes,shape,dictFrameTime):
        try:
            while True:

                frameTuple=q.get()
                if frameTuple==None:
                    break

                frameTime=frameTuple[0]
                frame=frameTuple[1]

                new_array = cv2.resize(frame, shape)
                p = new_array.reshape(-1, shape[0], shape[1], 3)
                try:
                    predection = numpy.argmax(model.predict([p]))
                    result_frame=classes[predection]
                    dictFrameTime[frameTime] = self.get_pose(result_frame)
                except Exception as ex:
                    print(str(ex))

               


        except Exception as ex:
            print(ex)

    
    def get_pose(self, file_name):
            head = Details.head.value
            leg = Details.leg.value
            wing = Details.wing.value
            tail = Details.tail.value
            center = Details.center.value
            right = Details.right.value
            left = Details.left.value
            down = Details.down.value
            up = Details.up.value
            off = Details.off.value
            on = Details.on.value
            none = Details.none.value

            # if we take just one name
            try:
                file_name_trimmed = file_name.replace(
                    '.', ':').replace('_', ',').lower()
                file_name_trimmed = ('{%s}' % file_name_trimmed)
                file_name_trimmed = eval(file_name_trimmed)
                return file_name_trimmed
            except Exception as ex:
                print(str(ex))
            

    def get_motion_per_time(self, dict_frame_time):
            head = Details.head.value
            leg = Details.leg.value
            wing = Details.wing.value
            tail = Details.tail.value
            center = Details.center.value
            right = Details.right.value
            left = Details.left.value
            down = Details.down.value
            up = Details.up.value
            off = Details.off.value
            on = Details.on.value
            none = Details.none.value


            row = dict({"Time": 0, "No Motion": '', "No Motion Time Span": '',
                        'head status': '',      "head movement": '', "head movement time span": '',
                        'leg status': '',       "leg movement": '', "leg movement time span": '',
                        'wing status': '',      "wing movement": '', "wing movement time span": '',
                        'tail status': '',       "tail movement": '', "tail movement time span": ''})
            
            tbl_movement = []
            dict_pose_change = {head: False, leg: False, wing: False, tail: False}
            dict_pose_start_time = {head: 0.0, leg: 0.0, wing: 0.0, tail: 0.0}
            dict_pose_end_time = {head: 0.0, leg: 0.0, wing: 0.0, tail: 0.0}
            list_of_sorted_keys = list(sorted(dict_frame_time))
            for index, cur_time in enumerate(sorted(dict_frame_time)):
                if len(dict_frame_time) - index == 1:
                    break
                else:
                    # birds_curr, birds_next are the dicts representing the pose of the bird
                    birds_pose_curr = dict_frame_time[cur_time]
                    next_time = list_of_sorted_keys[index+1]
                    birds_pose_next = dict_frame_time[next_time]

                    # if there is a diff create a new obj that contain a time
                    diff = self.get_difference(birds_pose_curr, birds_pose_next)

                    if diff is not None:
                        # new_row = None

                        for birdPart in diff.keys():

                            if not dict_pose_change[birdPart]:
                                # first move so record the start time
                                dict_pose_start_time[birdPart] = 0
                                dict_pose_change[birdPart] = True
                            else:
                                # if this the second move for the same part then record the end time
                                # and caculate the time interval of the move
                                dict_pose_end_time[birdPart] = next_time

      
                                new_row = row.copy()
                                time=Time.formulateTime(next_time)
                                new_row['Time'] = time
                                new_row[f"{str(birdPart)} status"] = f"{diff[birdPart]}"
                                new_row[f"{str(birdPart)} movement"] = f"{birds_pose_curr[birdPart]}-{diff[birdPart]}"
                                
                                motionTime=Time.subtractTimes(dict_pose_end_time[birdPart],dict_pose_start_time[birdPart])
                                new_row[f"{str(birdPart)} movement time span"] =motionTime


                                if (len(tbl_movement) != 0 and tbl_movement[len(tbl_movement)-1]['Time'] == new_row['Time']):
                                    if tbl_movement[len(tbl_movement)-1]['head movement'] == '' and new_row['head movement'] != '':
                                        tbl_movement[len( tbl_movement)-1]['head movement'] = new_row['head movement']
                                        tbl_movement[len( tbl_movement)-1]['head movement time span'] = new_row['head movement time span']
                                        tbl_movement[len( tbl_movement)-1]['head status'] = new_row['head status']
                                    
                                    if tbl_movement[len(tbl_movement)-1]['leg movement'] == '' and new_row['leg movement'] != '':
                                        tbl_movement[len(tbl_movement)-1]['leg movement'] = new_row['leg movement']
                                        tbl_movement[len(tbl_movement)-1]['leg movement time span'] = new_row['leg movement time span']
                                        tbl_movement[len( tbl_movement)-1]['leg status'] = new_row['leg status']

                                    if tbl_movement[len(tbl_movement)-1]['wing movement'] == '' and new_row['wing movement'] != '':
                                        tbl_movement[len(tbl_movement)-1]['wing movement'] = new_row['wing movement']
                                        tbl_movement[len(tbl_movement)-1]['wing movement time span'] = new_row['wing movement time span']
                                        tbl_movement[len(tbl_movement)-1]['wing status'] = new_row['wing status']

                                    if tbl_movement[len(tbl_movement)-1]['tail movement'] == '' and new_row['tail movement'] != '':
                                        tbl_movement[len(tbl_movement)-1]['tail movement'] = new_row['tail movement']
                                        tbl_movement[len(tbl_movement)-1]['tail movement time span'] = new_row['tail movement time span']
                                        tbl_movement[len( tbl_movement)-1]['tail status'] = new_row['tail status']
                                        
                                

                                else:
                                    tbl_movement.append(new_row)

                                dict_pose_start_time[birdPart] = next_time



                    

            self.excelQueue.put(tbl_movement)
            self.excelQueue.put(None)
            


    def get_difference(self, first_dict, second_dict):
        try:
            first_dict = set(first_dict.items())
            second_dict = set(second_dict.items())
            return dict(second_dict - first_dict)
        except:
            return None




    def run(self):
        try:
           dictFrameTime={}
        #  self.consume(self.queue,self.model,self.chunkSize,self.classes,self.shape)
           with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                for i in range(3):
                   executor.submit(self.consume, self.queue,self.model,self.classes,self.shape,dictFrameTime)

           self.get_motion_per_time(dictFrameTime)    

        except Exception as ex:
            print(str(ex))












#NOTe :inherent from the readucer

class ExcelWriter(threading.Thread,Readucer):
    def __init__(self,excelQueue,sheetPath):
        super().__init__()
        self.excelQueue=excelQueue
        self.sheetPath=sheetPath
        self.DictTotalTIme={}

    def TotalTimeCalc(self,listChange,sheetPath):
        try:

            head_motion_center = [d['head movement time span'] for d in listChange if 'head status' in d and d['head status'] == 'center']
            head_motion_left = [d['head movement time span'] for d in listChange if 'head status' in d and d['head status'] == 'left']
            head_motion_right = [d['head movement time span'] for d in listChange if 'head status' in d and d['head status'] == 'right']
            head_motion_none = [d['head movement time span'] for d in listChange if 'head status' in d and d['head status'] == 'none']

            wing_motion_on = [d['wing movement time span'] for d in listChange if 'wing status' in d and d['wing status'] == 'on']
            wing_motion_off = [d['wing movement time span'] for d in listChange if 'wing status' in d and d['wing status'] == 'off']
            wing_motion_none = [d['wing movement time span'] for d in listChange if 'wing status' in d and d['wing status'] == 'none']

            leg_motion_up = [d['leg movement time span'] for d in listChange if 'leg status' in d and d['leg status'] == 'up']
            leg_motion_down = [d['leg movement time span'] for d in listChange if 'leg status' in d and d['leg status'] == 'down']
            leg_motion_none = [d['leg movement time span'] for d in listChange if 'leg status' in d and d['leg status'] == 'none']

            tail_motion_center = [d['tail movement time span'] for d in listChange if 'tail status' in d and d['tail status'] == 'center']
            tail_motion_none = [d['tail movement time span'] for d in listChange if 'tail status' in d and d['tail status'] == 'none']

            head_center=0
            head_left=0
            head_right=0
            head_none=0
            for i in head_motion_center:
                head_center+=Time.reverseFormulateTime(i)
            head_center=Time.formulateTime(head_center)

            for i in head_motion_left:
                head_left+=Time.reverseFormulateTime(i)
            head_left=Time.formulateTime(head_left)

            for i in head_motion_right:
                head_right+=Time.reverseFormulateTime(i)
            head_right=Time.formulateTime(head_right)
    
            for i in head_motion_none:
                head_none+=Time.reverseFormulateTime(i)
            head_none=Time.formulateTime(head_none)


            wing_on=0
            wing_off=0
            wing_none=0
            for i in wing_motion_on:
                wing_on+=Time.reverseFormulateTime(i)
            wing_on=Time.formulateTime(wing_on)

            for i in wing_motion_off:
                wing_off+=Time.reverseFormulateTime(i)
            wing_off=Time.formulateTime(wing_off)


            for i in wing_motion_none:
                wing_none+=Time.reverseFormulateTime(i)
            wing_none=Time.formulateTime(wing_none)


            leg_up=0
            leg_down=0
            leg_none=0
            for i in leg_motion_up:
                leg_up+=Time.reverseFormulateTime(i)
            leg_up=Time.formulateTime(leg_up)

            for i in leg_motion_down:
                leg_down+=Time.reverseFormulateTime(i)
            leg_down=Time.formulateTime(leg_down)


            for i in leg_motion_none:
                leg_none+=Time.reverseFormulateTime(i)
            leg_none=Time.formulateTime(leg_none)

            tail_center=0
            tail_none=0
            for i in tail_motion_center:
                tail_center+=Time.reverseFormulateTime(i)
            tail_center=Time.formulateTime(tail_center)


            for i in tail_motion_none:
                tail_none+=Time.reverseFormulateTime(i)
            tail_none=Time.formulateTime(tail_none)

            data = {'Body Part': ['head', 'head', 'head', 'head','wing','wing','wing','leg','leg','leg','tail','tail'],
                    'Status':   ['center', 'left', 'right','none','on','off','none','down','up','none','center','none'],
                    'Total Time': [head_center, head_left, head_right, head_none,wing_on,wing_off,wing_none,leg_down,leg_up,leg_none,tail_center,tail_none]
                    }

            # create data frame
            df = pd.DataFrame(data).set_index("Body Part")

            with pd.ExcelWriter(sheetPath, engine='openpyxl', mode='a',if_sheet_exists='overlay') as writer:
                        df.to_excel(writer, sheet_name="Total Time Statistcs")
        except Exception as ex:
            print(str(ex))
                        
        



    def readuce(self, changeq,sheetPath):
        try:
            while True:
                
                change=changeq.get()
                # print(change) 
                if change==None:
                    break  
                if len(change) == 0:
                    print("EcelWriter: There is no motion happend in this chunk !!")
                    return
                
                export_details = pd.DataFrame(change).set_index("Time")

                export_details.columns = ["No Motion", "No Motion\n Time Span (sec)",
                                        'head status', "head movement", "head movement\n time span",
                                        'leg status',  "leg movement", "leg movement\n  time span",
                                        'wing status',   "wing movement", "wing movement\n  time span",
                                        'tail status',    "tail movement", "tail movement\n  time span"]
                
                if not os.path.exists(self.sheetPath):
                    with pd.ExcelWriter(sheetPath, engine='openpyxl') as writer:
                        export_details.to_excel(writer, sheet_name="Details")
                else:
                    with pd.ExcelWriter(sheetPath, engine='openpyxl', mode='a',if_sheet_exists='overlay') as writer:
                        export_details.to_excel(writer, sheet_name="Details", startrow=writer.sheets['Details'].max_row, header=False)
                self.TotalTimeCalc(change,sheetPath)
                print("EcelWriter: Exporting data done succesfully.")       
        except Exception as ex:
            print(ex)
    
    def run(self):
        try:
    
                
                # movements=self.excelQueue.get()
            # self.Export2Excel(self.excelQueue)
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
               executor.submit(self.readuce, self.excelQueue,self.sheetPath)
       
        except Exception as ex:
            print(str(Exception))
        
        


if __name__ == '__main__':
    q=Queue()
    ExcelQ=Queue()
    DependcisQ=Queue()
    modelPath=r"D:\Modeling\Traning_Model\chronic crow 2nd green blue object novelty TS h.h5" #Training model path - Change to your pc path  
    shape=(128,128)
    
    folder_path="D:\Modeling\Frames\chronic crow 2nd green blue object novelty TS h" #Path for frames folder - Change to your pc path  
    folder_list=[]

    for folder in os.listdir(folder_path):
    	if os.path.isdir(os.path.join(folder_path,folder)):
        	folder_list.append(folder)
    	else:
        	print("Incorrect Path !!")
        
    classes=folder_list
    
    video_name='chronic crow 2nd green blue object novelty TS h' #Video name - Change to your video name  
    sheet_path="D:\Modeling" #Path to save excel sheet - Change to your pc path  
    videoPath=r"D:\Modeling\Video\chronic crow 2nd green blue object novelty TS h.mp4" #path to video - Change to your pc path  
    
    sheet=r"{}\{}.xlsx".format(sheet_path,video_name)
    P=VideoProducer(q,DependcisQ,videoPath,modelPath,classes,shape)
    C=Consumer(q, DependcisQ,ExcelQ)
    W=ExcelWriter(ExcelQ,sheet)
    P.start()
    C.start()
    W.start()

    P.join()
    C.join()
    W.join()

    