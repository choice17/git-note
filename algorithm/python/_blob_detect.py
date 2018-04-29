import numpy as np
import matplotlib.pyplot as plt 

#%%
"""
algorithm for connected-graph 
two pass algorithm for binary image
"""

class Connected_algo:
        
           
    def binarize_img(im_name):
        """
        binarize_img is to turn rgb image to one dimension binary value
        im_name: string of image path
        """
        img = plt.imread(im_name)
        b_img = np.zeros([10,10])
        
        for i in range(0,3):
            b_img += img[:,:,i]
        
        b_img[b_img<100] = 1
        b_img[b_img>100] = 0
        return b_img

               
        
    def two_pass(img):
        """
        two pass connected-components algo for image, output connected-components
        img: binary 0/1 img
        
        """
        def find_neighbor(img,idx):
        
            neighbors = []
            im_rows, im_cols = img.shape
            row, col = idx
            # position definition
            pos = {'a':(row-1,col-1),'b':(row-1,col),'c':(row-1,col+1),'d':(row,col-1)}
            
            if (row==0 and col==0) :
                return []
            if (row==0):
                if img[pos['d']] != 0:
                    neighbors.append((pos['d'],img[pos['d']]))
                    return neighbors
                else:
                    return []
            if (col==0):
                for row_,col_ in [pos['b']]:#pos['c']):
                    if (img[row_,col_] != 0):
                        neighbors.append(([row_,col_],img[row_,col_]))
                return neighbors
            
    
            if (col==im_cols-1):
            #    for row_,col_ in (pos['a'],pos['b'],pos['d']):
                for row_,col_ in (pos['b'],pos['d']):
                    if img[row_,col_] != 0:
                        neighbors.append(([row_,col_],img[row_,col_]))
                return neighbors    
            
            #for row_,col_ in pos.values():
            for row_,col_ in (pos['b'],pos['d']):
                if img[row_,col_] != 0:
                    neighbors.append(([row_,col_],img[row_,col_]))
            return neighbors
            
        linked = {}
        
        rows, cols = img.shape
        marks = img.copy()
        next_label = 1
        
        #first pass
        for row in range(rows):
            for col in range(cols):
                if img[row,col] != 0:
                    neighbors = find_neighbor(marks,[row,col])
                    
                    if neighbors is None or neighbors == []:
                        marks[row,col] = next_label
                        next_label = next_label+1
                    else:
                        #print(neighbors)
                        try:
                            grps = [grp for _,grp in neighbors] 
                            cur_label = np.min(grps)
                            marks[row,col] = cur_label
                        
                            grps = set(grps)                            
                            if linked.get(cur_label) is None:
                                linked[cur_label] = set(grps)
                            else:
                                linked[cur_label]  = linked[cur_label].union(set(grps))
                        except (RuntimeError, TypeError, NameError) as e:
                            print(e)
                            
                            #print('error :', neighbors)
                            
        #second pass
        for label in np.sort(list(linked.keys()))[::-1]:
            for label_ in linked[label]:
                if label != label_:                    
                    marks[marks==label_]=label
        #relabel
        marks_ = np.zeros(marks.shape)
        for idx,label in enumerate(set(marks.flatten())):            
            if idx != 0.0:
                marks_[marks==label]=idx        
        
        return marks_
        
        
                    
#%% test command

if __name__ == "__main__":
    
    im_name = "blob.jpg"
    b_img = Connected_algo.binarize_img(im_name)

    d_img = b_img
    c_img = Connected_algo.two_pass(d_img)


    _,axes = plt.subplots(1, 2)
    axes[0].imshow(b_img)
    axes[1].imshow(c_img)
    plt.show()
    
