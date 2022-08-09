import cv2
import numpy as np


#import cv2 for breaking images down to pixels or continuous arrays
img = cv2.imread('test_image.jpg')
#It's imparative to make a copy of image, in
lane_img = np.copy(img)

def canny(image):
    #To convert the color of image from a RGB to grayscale
    #cuz the number of channel of a RGB image is 3, whereas grayscale channel is 1,
    #Thus grayscale image enables to run itself faster than RGB
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    #for reducing the noises of the image, we use GaussianBlur
    #in which the algorhthm takes averages of the adjacent pixels and 
    #average them
    blur = cv2.GaussianBlur(gray,(5,5),0)
    #isolate the edge in images, we are using the derivative of the adjacent pixels
    #thus we know the slope of specific points 
    #images are arrays of consective pixels, 
    # we can denote like this pixel = (x,y)
    #if a griedient of the adjacent pixels is lower than lowest_thrushhold
    #It'll be ingored 
    #if a griedient of the adjacent pixels is higher than highest_thrushhold
    #It's gonna be itentified as an edge
    #If a gredient of adjacent pixels is between lowest and highest_thrushhold
    #It'll be identified as edges, only if it's placed next to the edges
    #The documentation recommends to use the ratio of thrushholds 1:3
    canny = cv2.Canny(blur,50,150)
    return canny


def region_of_interest(image):
    #to limit our images for an extent where we can identify lanes
    #first, we specify the area of images 

    #get the rows from image's shape
    height = image.shape[0]
    #specify the cordinates where you want to idetify objects
    polygons = np.array([
    [(200,height),(1100,height),(550,250)]
    ])
    #then make a copy of image in black, then mask with the polygon we made above
    mask = np.zeros_like(image)
    cv2.fillPoly(mask,polygons,255)
    
    #8 bit binary representation's maximum number that can show
    # is 255. When a pixel is completely black, the binary representation
    # should be 00000000. When we operate bitwise-and to the corresponding
    # region of the other image, All of the pixels which are at same matrix
    # will be all zero(0). Cause in bitwise-and 1 applied only if the bit value
    # of two images are both 1, otherwise 0. 
    masked_image= cv2.bitwise_and(mask,image)
    
    # lines detection
    # we detect lines in region of interest.
    # lines are a series of dots. then to find the line's equasion by using 
    # hough line, which detects intersections --with params (radians,distance)
    # the line pass through the dots/points 
    # divided houghline to bins, then take the most intersections including bin
    # the params in that bin tends to pass  
    lines = cv2.HoughLinesP(masked_image,2,np.pi/180,100,np.array([]),minLineLength = 40, maxLineGap =5)
    return masked_image,lines

def lines_onto_black_image(image,lines):
    #create completely black image with the same dimention as image
    lines_onto_black_image = np.zeros_like(image)
    #just confirm that we detected the lines with houghlinep
    if lines is not None:
        for l in lines:
            # raw coordinates are 3 dimentional array like below
                #[[[,,,,]]
                # [[,,,,]]
                # ]
            # in for loop these convert to 2 dimentions
            # then we wanna use 1 dimention, 4 coordinates then reshape
            x1,y1,x2,y2 = l.reshape(4)
            # after that cv2.line allows us to draw lines between 2 points (x1,y1),(x2,y2)
            cv2.line(lines_onto_black_image,(x1,y1),(x2,y2),(255,0,0),10)
        return lines_onto_black_image
    
def average_slope_intercept(image,lines):
    # for smoothing the lines
    # average slope and intercept
    left_line = []
    right_line = []
    
    for l in lines:
        x1,y1,x2,y2 = l.reshape(4)
        #polyfit returns first degree polynomial's coefficients
        #but depending on argument of deg(degree)
        #first degree means the equation with 1 exponential
        paramators = np.polyfit((x1,x2),(y1,y2),1)
        slope = paramators[0]
        intercepts = paramators[1]
    
    #as for this image, two lines slanted to the right, and left respectively
    #y axis of image from the top of left side downward to the bottum of left
    #so the slope of the line slanted to the right is negative
    #the slope of the line slanted to the left is positive
        if slope < 0:
            left_line.append((slope, intercepts))
        else:
            right_line.append((slope, intercepts))
    #then average out each slope and intercepts respectively
    left_line_average = np.average(left_line,axis=0)
    right_line_average = np.average(right_line,axis=0)
    ave_left_line = get_coordinates(image,left_line_average)
    ave_right_line = get_coordinates(image,right_line_average)
    #[308 704 483 422] [978 704 703 422]
    #as seen above, returned values are the coordinates of each line--left/right
    return ave_left_line, ave_right_line
    
def get_coordinates(image,line_params):
    slope, intercepts = line_params
    y1 = image.shape[0]
    y2 = int(y1*3/5)
    x1 = int((y1-intercepts)/slope)
    x2 = int((y2-intercepts)/slope)
    return np.array([x1,y1,x2,y2])

# canny = canny(lane_img)

# masked_image,lines = region_of_interest(canny)
# averaged_lines = average_slope_intercept(lane_image,lines)
# lines_onto_black_image = lines_onto_black_image(lane_img,averaged_lines)
# #blend the first lane_image and the lines_image
# #in lines_image whole region is black other than lines 
# #it means pixels intensities equal to 0
# #therefore adding pixels intensities of black space won't make
# #any differences, only when add the intensities of lines we can cee
# #them on raw images
# blended_image = cv2.addWeighted(lane_img,0.8, lines_onto_black_image,1,1)

# cv2.imshow('lanes',blended_image )
# cv2.waitKey(0)


#video line detection 
#capture the video, and while it's run as each single frame
#detect and get 2 values(boolean, frame)
cap = cv2.VideoCapture('test2.mp4')
while(cap.isOpened()):
    ret,frame = cap.read()
    if ret == True:
        # then detect lines and project it on video frame/image
        # Just changed the input image from lane_image to frame
        # canny = canny(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        canny = cv2.Canny(blur,50,150)

        #to limit our images for the extent where we can identify lanes
        #first, we specify the area of images 

        #get the rows from image's shape
        height = canny.shape[0]
        #specify the cordinates where we want to idetify objects
        polygons = np.array([
        [(200,height),(1100,height),(550,250)]
        ])
        #then make a copy of image in black, then mask with the polygon we made above
        mask = np.zeros_like(canny)
        cv2.fillPoly(mask,polygons,255)
        
        #8 bit binary representation's maximum number that can show
        # is 255. When a pixel is completely black, the binary representation
        # should be 00000000. When we operate bitwise-and to the corresponding
        # region of the other image, All of the pixels which are at same matrix
        # will be all zero(0). Cause in bitwise-and 1 applied only if the bit value
        # of two images are both 1, otherwise 0. 
        masked_image= cv2.bitwise_and(mask,canny)
        
        # lines detection
        # we detect lines in region of interest.
        # lines are a series of dots. then to find the line's equasion by using 
        # hough line, which detects intersections --with params (radians,distance)
        # the line pass through the dots/points 
        # divided houghline to bins, then take the bin that includes intersections the most
        # the params in that bin tends to pass lines more than other bins do
        lines = cv2.HoughLinesP(masked_image,2,np.pi/180,100,np.array([]),minLineLength = 40, maxLineGap =5)
        averaged_lines = average_slope_intercept(frame,lines)
        # lines_onto_black_image = lines_onto_black_image(frame,averaged_lines)
        
            #create completely black image with the same dimention as image
        black_image = np.zeros_like(frame)
    #just confirm that we detected the lines with houghlinep
        if lines is not None:
            for l in lines:
                # raw coordinates are 3 dimentional array like below
                    #[[[,,,,]]
                    # [[,,,,]]
                    # ]
                # in for loop these convert to 2 dimentions
                # then we wanna use 1 dimention, 4 coordinates then reshape
                x1,y1,x2,y2 = l.reshape(4)
                # after that cv2.line allows us to draw lines between 2 points (x1,y1),(x2,y2)
                cv2.line(black_image,(x1,y1),(x2,y2),(255,0,0),10)
        #blend the first lane_image and the lines_image
        #in lines_image whole region is black other than lines 
        #it means pixels intensities equal to 0
        #therefore adding pixels intensities of black space won't make
        #any differences, unless the intensities of lines were added
        blended_image = cv2.addWeighted(frame,0.8, black_image,1,1)

        cv2.imshow('lanes',blended_image )
    # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

  # Break the loop
    else:
        break

# When everything done, release the video capture object

cap.release()
# Closes all the frames

cv2.destroyAllWindows()
