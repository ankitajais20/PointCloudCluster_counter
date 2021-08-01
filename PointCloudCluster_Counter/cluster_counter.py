#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
import math

def callback(msg):
    cluster=[]  #list to store no. of points there in all the clusters
    i=0
    infinity = float('inf') 
#following loop to find out the first point while starting from 0 degree
    for j in range(360):
        if msg.ranges[j]!=infinity:    
             i=j
             break
# initialisinig the first point i.e. x0 and y0 
    theta=msg.angle_min+i*msg.angle_increment
    x0=x=msg.ranges[i]*math.cos(theta)
    y0=y=msg.ranges[i]*math.sin(theta)
    i+=1
    points=1
    n=-1
    empty=0
#loop to compare distance between subsequents points and find out the distance b/w them and if distance is less than threshold distance they are of same cluster
    for j in range(i,360):
        if msg.ranges[j]!=infinity:
           theta=msg.angle_min+j*msg.angle_increment 
           x1=msg.ranges[j]*math.cos(theta)
           y1=msg.ranges[j]*math.sin(theta) 
           d =math.sqrt(pow((x1-x),2)+pow((y1-y),2)) 
           if d< 0.25 :    #threshold distance taken as 0.25
              points+=1
           else :
#if distance between the end points of two adjacent clusters is more than width of the turtlebot then we can call it as an empty space through which the bot can pass
              if d>0.31 :  #width may be taken accordingly, for waffle_pi, width is 0.31m (approx.) and for burger, width can be taken as 0.18m (approx.)  
                 empty+=1
              cluster.append(points)
              points=1
              n+=1
           x=x1
           y=y1
    d1=math.sqrt(pow((x-x0),2)+pow((y-y0),2)) #calculating distance b/w the first and last point in a 360 degree rotation since they might be of the same cluster 
    if d1<0.25 :                                #if they are of same cluster then reduce the number of clusters by 1
       cluster[0]=cluster[0]+cluster[n]
       cluster.pop(n)
    elif d1>0.31 :
       empty+=1

################################################################
    print ("Total no. of clusters: "+str(len(cluster)))
    for j in range(len(cluster)):
         print("No. of points in cluster "+str(j+1)+" is: "+str(cluster[j]))
    print ("Total no. of empty spaces through which the turtlebot can pass: "+str(empty))


rospy.init_node("PointCloudCluster")
sub = rospy.Subscriber('/scan', LaserScan, callback)
rospy.spin()
