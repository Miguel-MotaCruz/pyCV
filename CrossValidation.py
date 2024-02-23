


import numpy as np

import arff
import random
import pandas as pd



class CrossValidation:



    def __init__(self,file_name,distance_func="default",file_type="arff"):
        '''
        Constructor method, setups up the the necessary class attributes to be
        used by the complexity measure functions.
        Starts by reading the file in arff format which contains the class samples X (self.X), class labels y (self.y) and contextual information
        about the features (self.meta).
        It also saves in an array the unique labels of all existing classes (self.classes), the number of samples in each class (self.class_count) and
        the indexes in X of every class (self.class_inxs).
        -----
        Parameters:
        file_name (string): Location of the file that contains the dataset.
        distance_func (string): The distance function to be used to calculate the distance matrix. Only available option right now is "HEOM".
        file_type (string): The type of file where the dataset is stored. Only available option right now is "arff".
        
        '''
        if(file_type=="arff"):
            [X,y,meta,class_inds]=self.__read_file(file_name)
        else:
            print("Only arff files are available for now")
            return

        self.X=np.array(X)
        self.y=np.array(y)
        self.classes=np.unique(self.y)
        self.meta=meta
        #self.dist_matrix,self.unnorm_dist_matrix = self.__calculate_distance_matrix(self.X,distance_func=distance_func)
        #self.class_count = self.__count_class_instances()


        self.class_inxs = class_inds


        self.class_count = self.__count_class_instances()
        if(len(self.class_count)<2):
           print("ERROR: Less than two classes are in the dataset.")

        return 

    def __count_class_instances(self):
        '''
        Is called by the __init__ method.
        Count instances of each class in the dataset.
        --------
        Returns:
        class_count (numpy.array): An (Nx1) array with the number of intances for each of the N classes in the dataset 
        '''
        class_count = np.zeros(len(self.classes))
        for i in range(len(self.classes)):
            count=len(np.where(self.y == self.classes[i])[0])
            class_count[i]+=count
        return class_count


    def __read_file(self,file):
        data = arff.load(open(file, 'r'))['data']
        num_attr = len(data[0])-1
        att=arff.load(open(file, 'r'))['attributes']
        meta=[]
        for i in range(len(att)-1):
            if(att[i][1]=="NUMERIC"):
                meta.append(0)
            else:
                meta.append(1)


        X = np.array([i[:num_attr] for i in data])
        y = np.array([i[-1] for i in data])


        X = np.array(X)
        for i in range(len(meta)):
            if meta[i]==1:
                
                b, c = np.unique(X[:,i], return_inverse=True)
                X[:,i] = c

        if 1 in meta:
            X = X.astype(np.float64)




        classes = np.unique(y)
        y = [np.where(classes == i[-1])[0][0] for i in data]
        classes = np.unique(y)
        

        class_inds = []
        for cls in classes:
            cls_ind=np.where(y==cls)[0]
            class_inds.append(cls_ind)
        


        X = np.array(X)
        y = np.array(y)
        

        return [X,y,meta,class_inds]
    


    def __distance_HEOM(self,X):
        '''
        Is called by the calculate_distance_matrix method.
        Calculates the distance matrix between all pairs of points from an input matrix, using the HEOM metric, that way categorical attributes are
        allow in the dataset.
        --------
        Parameters: 
        X (numpy.array): An (N*M) numpy matrix containing the points, where N is the number of points and M is the number of attributes per point.
        --------
        Returns:
        dist_matrix (numpy.array): A (M*M) matrix containing the distance between all pairs of points in X
        '''
        
        
        meta = self.meta
        dist_matrix=np.zeros((len(X),len(X)))
        unnorm_dist_matrix = np.zeros((len(X),len(X)))

        #calculate the ranges of all attributes
        range_max=np.max(X,axis=0)
        range_min=np.min(X,axis=0)
        #print(range_max)
        #print(range_min)
        for i in range(len(X)): 
            for j in range(i+1,len(X)):
                #for attribute
                dist = 0
                unnorm_dist = 0
                for k in range(len(X[0])):
                    #missing value
                    if(X[i][k] == None or X[j][k]==None):
                        dist+=1
                        unnorm_dist+=1
                    #numerical
                    if(meta[k]==0):
                        #dist+=(abs(X[i][k]-X[j][k]))**2
                        
                        #dist+=(abs(X[i][k]-X[j][k])/(range_max[k]-range_min[k]))**2
                        if(range_max[k]==range_min[k]):
                            dist+=(abs(X[i][k]-X[j][k]))**2
                            unnorm_dist+=(abs(X[i][k]-X[j][k]))**2
                        else:
                            dist+=(abs(X[i][k]-X[j][k])/(range_max[k]-range_min[k]))**2
                            unnorm_dist+= abs(X[i][k]-X[j][k])**2
                            
                            #dist+=(abs(X[i][k]-X[j][k]))**2
                    #categorical
                    if(meta[k]==1):
                        if(X[i][k]!=X[j][k]):
                            dist+=1
                            unnorm_dist+=1

                dist_matrix[i][j]=np.sqrt(dist)
                dist_matrix[j][i]=np.sqrt(dist)

                unnorm_dist_matrix[i][j]=np.sqrt(unnorm_dist)
                unnorm_dist_matrix[j][i]=np.sqrt(unnorm_dist)
        #print(dist_matrix)
        return dist_matrix,unnorm_dist_matrix
    


    def __calculate_distance_matrix(self,X,distance_func="HEOM"):
        '''
        Is called by the __init__ method.
        Function used to select which distance metric will be used to calculate the distance between a matrix of points.
        Only the HEOM metric is implemented for now, however if more metrics are added this function can easily be changed to
        incomporate the new metrics.
        --------
        Parameters:
        X (numpy.array): An (N*M) numpy matrix containing the points, where N is the number of points and M is the number of attributes per point.
        distance_func (string): The distance function to be used, only available option right now is "HEOM"
        --------
        Returns:
        dist_matrix (numpy.array): A (M*M) matrix containing the distance between all pairs of points in X
        --------
        '''
        if(distance_func=="HEOM"):
            distance_matrix,unnorm_distance_matrix=self.__distance_HEOM()
        elif(distance_func=="default"):
            distance_matrix,unnorm_distance_matrix=self.__distance_HEOM()
        
        #add other distance functions

        return distance_matrix,unnorm_distance_matrix
    
    
    def __write_arff(self,X_res,y_res,output_folder,file):
        X_res = pd.DataFrame(X_res)
        y_res = [int(round(numeric_string)) for numeric_string in y_res]
        y_res = pd.DataFrame(y_res)
        

        
        #print(y_res)
        y_res = pd.DataFrame(y_res)
        
        y_res.rename(columns = {0 : 'class'}, inplace = True)
        df =  X_res.join(y_res)

        #print(df)
        attributes = [(str(j), 'NUMERIC') if X_res[j].dtypes in ['int64', 'float64'] else (j, X_res[j].unique().astype(str).tolist()) for j in X_res]
        attributes += [('label',['0.0','1.0'])]


        arff_dic = {
                'attributes': attributes,
                'data': df.values,
                'relation': 'myRel',
                'description': ''
                }
        #print(arff_dic)
        
        #new_name = file.split(".")[0]  + ".arff"
        with open(output_folder + file + ".arff", "w", encoding="utf8") as f:
            arff.dump(arff_dic, f)

    def write_folds(self,folds,folds_y,filename,folder):
        training_partitions = []
        testing_partitions = []
        for i in range(len(folds)):

            train_fold_X=[]
            test_fold_X = np.array(folds[i])

            train_fold_y=[]
            test_fold_y= np.array(folds_y[i])

            for j in range(len(folds)):

                if(j!=i):
                
                    if(len(train_fold_X)==0):
                        train_fold_X = folds[j]
                        train_fold_y = folds_y[j]
                    else:
                        train_fold_X = np.append(train_fold_X,folds[j],axis=0)
                        train_fold_y = np.append(train_fold_y,folds_y[j])


            training_partitions.append(train_fold_X)
            testing_partitions.append(test_fold_X)

            #name_tra = file.split(".")[0] + "-" + cv_algorithm +"-V" + str(v) + "-" + str(fold_num) + "-" + str(i+1) + "tra.arff" 
            #name_tst = file.split(".")[0] + "-" + cv_algorithm +"-V" + str(v) + "-" + str(fold_num) + "-" + str(i+1) + "tst.arff" 

            name_tra = filename + "-" + str(len(folds)) + "-" + str(i+1) + "tra"
            name_tst = filename + "-" + str(len(folds)) + "-" + str(i+1) + "tst"
            self.__write_arff(train_fold_X,train_fold_y,folder,name_tra)
            self.__write_arff(test_fold_X,test_fold_y,folder,name_tst)
    


    def getClosest(self,pos,dist_matrix):

        #select closest sample 
        #in case of the first row the value has to be different
        if(pos!=0):
            min_val = dist_matrix[pos][0]
            new_pos = 0
        else:
            min_val = dist_matrix[pos][1]
            new_pos = 1
        

        for i in range(len(dist_matrix[pos])):
            #check if not itself
            if i!=pos:
                if dist_matrix[pos][i] < min_val:
                    min_val = dist_matrix[pos][i]
                    new_pos = i
            #get min


        #remove sample from dist matrix
        return new_pos
    


    def getMostDistant(self,pos,dist_matrix):

        #select closest sample 
        #in case of the first row the value has to be different
        if(pos!=0):
            min_val = dist_matrix[pos][0]
            new_pos = 0
        else:
            min_val = dist_matrix[pos][1]
            new_pos = 1
        

        for i in range(len(dist_matrix[pos])):
            #check if not itself
            if i!=pos:
                if dist_matrix[pos][i] > min_val:
                    min_val = dist_matrix[pos][i]
                    new_pos = i
            #get min


        #remove sample from dist matrix
        return new_pos


    def SCV(self,foldNum=5):
        folds = []
        folds_y = []
        folds_inx = []

        for i in range(foldNum):
            folds.append([])
            folds_y.append([])
            folds_inx.append([])


        class_inxs = self.class_inxs
        

        for c_count in range(len(self.classes)):
            X_cls = self.X[class_inxs[c_count]]
            y_cls = self.y[class_inxs[c_count]]
            cls_inxs = class_inxs[c_count]


            orgCount = len(cls_inxs)
            for i in range(foldNum):
                
                n = orgCount//foldNum
                for j in range(0,n):
                    pos = random.randint(0,len(X_cls)-1)
                    
                    folds[i].append(X_cls[pos])
                    folds_y[i].append(y_cls[pos])
                    folds_inx[i].append(cls_inxs[pos])
                    
                    X_cls = np.delete(X_cls, (pos), axis=0)
                    y_cls = np.delete(y_cls, (pos), axis=0)
                    cls_inxs = np.delete(cls_inxs, (pos), axis=0)

                if(orgCount%foldNum>i):


                    pos = random.randint(0,len(X_cls)-1)

                    folds[i].append(X_cls[pos])
                    folds_y[i].append(y_cls[pos])
                    folds_inx[i].append(cls_inxs[pos])

                    X_cls = np.delete(X_cls, (pos), axis=0)
                    y_cls = np.delete(y_cls, (pos), axis=0)
                    cls_inxs = np.delete(cls_inxs, (pos), axis=0)
                

        return folds,folds_y,folds_inx

           



    def DBSCV(self,foldNum=5):
        folds = []
        folds_y = []
        folds_inx = []
        

        class_inxs = self.class_inxs
       
        
        for i in range(foldNum):
            folds.append([])
            folds_y.append([])
            folds_inx.append([])

        
        for c_count in range(len(self.classes)):
            X_cls = self.X[class_inxs[c_count]]
            y_cls = self.y[class_inxs[c_count]]
            cls_inxs = class_inxs[c_count]

            
            dist_matrix_cls,unnorm_dist_matrix_cls = self.__distance_HEOM(X_cls)
                
            i = 0
            cnt=len(X_cls)
            
            pos = random.randint(0,len(X_cls)-1)
            sample = X_cls[pos]
            sample_y = y_cls[pos]

            while(cnt>1): 
                folds[i].append(sample)
                folds_y[i].append(sample_y)
                folds_inx[i].append(cls_inxs[pos])
                
                
                
                cnt = cnt-1
                i = (i+1)%foldNum


                #remove from dataset
                X_cls = np.delete(X_cls, (pos), axis=0)
                y_cls = np.delete(y_cls, (pos), axis=0)
                cls_inxs = np.delete(cls_inxs, (pos), axis=0)

                new_pos = self.getClosest(pos,dist_matrix_cls)
                

                #remove form dist matrix
                dist_matrix_cls = np.delete(dist_matrix_cls, (pos), axis=0)
                dist_matrix_cls = np.delete(dist_matrix_cls, (pos), axis=1)
                

                if(new_pos > pos):
                    pos = new_pos-1
                else:
                    pos = new_pos

                sample = X_cls[pos]
                sample_y = y_cls[pos]

            folds[i].append(sample)
            folds_y[i].append(sample_y)        
            folds_inx[i].append(cls_inxs[pos])    

        return folds,folds_y,folds_inx
    
    def DOBSCV(self,foldNum=5):
        folds = []
        folds_y = []
        folds_inx = []

        for i in range(foldNum):
            folds.append([])
            folds_y.append([])
            folds_inx.append([])


        class_inxs = self.class_inxs
        
        for c_count in range(len(self.classes)):
            X_cls = self.X[class_inxs[c_count]]
            y_cls = self.y[class_inxs[c_count]]
            dist_matrix_cls,unnorm_dist_matrix_cls = self.__distance_HEOM(X_cls)
            cls_inxs = class_inxs[c_count]

            
            cnt=len(X_cls)

            while(cnt>0): 


                pos = random.randint(0,len(X_cls)-1)
                sample = X_cls[pos]
                sample_y = y_cls[pos]


                folds[0].append(sample)
                folds_y[0].append(sample_y)
                folds_inx[0].append(cls_inxs[pos])
                
                
                
                cnt = cnt-1

                
                if(cnt==0):
                    break
                    
                

                for i in range(1,foldNum):
                    p2 = self.getClosest(pos,dist_matrix_cls)


                
                    folds[i].append(X_cls[p2])
                    folds_y[i].append(y_cls[p2])
                    folds_inx[i].append(cls_inxs[p2])

                    X_cls = np.delete(X_cls, (p2), axis=0)
                    y_cls = np.delete(y_cls, (p2), axis=0)
                    cls_inxs = np.delete(cls_inxs, (p2), axis=0)

                    dist_matrix_cls = np.delete(dist_matrix_cls, (p2), axis=0)
                    dist_matrix_cls = np.delete(dist_matrix_cls, (p2), axis=1)

                    cnt = cnt-1

                    if(p2 < pos):
                        pos = pos-1
                    


                    if(cnt==0):
                        break

                if(cnt==0):
                    break    

                dist_matrix_cls = np.delete(dist_matrix_cls, (pos), axis=0)
                dist_matrix_cls = np.delete(dist_matrix_cls, (pos), axis=1)

                X_cls = np.delete(X_cls, (pos), axis=0)
                y_cls = np.delete(y_cls, (pos), axis=0)
                cls_inxs = np.delete(cls_inxs, (pos), axis=0)

        return folds,folds_y,folds_inx

    def MSSCV(self,foldNum=5):
        folds = []
        folds_y = []
        folds_inx = []
        

        class_inxs = self.class_inxs
       
        
        for i in range(foldNum):
            folds.append([])
            folds_y.append([])
            folds_inx.append([])

        
        for c_count in range(len(self.classes)):
            X_cls = self.X[class_inxs[c_count]]
            y_cls = self.y[class_inxs[c_count]]
            cls_inxs = class_inxs[c_count]

            
            dist_matrix_cls,unnorm_dist_matrix_cls = self.__distance_HEOM(X_cls)
                
            i = 0
            cnt=len(X_cls)
            
            pos = random.randint(0,len(X_cls)-1)
            sample = X_cls[pos]
            sample_y = y_cls[pos]

            while(cnt>1): 
                folds[i].append(sample)
                folds_y[i].append(sample_y)
                folds_inx[i].append(cls_inxs[pos])
                
                
                
                cnt = cnt-1
                i = (i+1)%foldNum


                #remove from dataset
                X_cls = np.delete(X_cls, (pos), axis=0)
                y_cls = np.delete(y_cls, (pos), axis=0)
                cls_inxs = np.delete(cls_inxs, (pos), axis=0)

                new_pos = self.getMostDistant(pos,dist_matrix_cls)
                

                #remove form dist matrix
                dist_matrix_cls = np.delete(dist_matrix_cls, (pos), axis=0)
                dist_matrix_cls = np.delete(dist_matrix_cls, (pos), axis=1)
                

                if(new_pos > pos):
                    pos = new_pos-1
                else:
                    pos = new_pos

                sample = X_cls[pos]
                sample_y = y_cls[pos]

            folds[i].append(sample)
            folds_y[i].append(sample_y)        
            folds_inx[i].append(cls_inxs[pos])    

        return folds,folds_y,folds_inx