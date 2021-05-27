#for script to work all blocks must be defined in drawing and title block must exist

import rhinoscriptsyntax as rs
import csv
import os

#set directory for CSV files
os.chdir('C:\Users\Mark M\Desktop')
  
# opening the CSV file and store notes in a list
def import_notes(file): 
    with open(file, mode ='r')as file: 
      csv_file = csv.reader(file) 
      notes = []
      for line in csv_file: 
            notes.append(line) 
      return notes

#layer function for putting geometry on correct layers
def layer(name):
    if not rs.IsLayer(name):
        rs.AddLayer(name)
    rs.CurrentLayer(name)

#create overall opening and points for hinges based on # of hinges
def opening(x,y,num_hinges=2):
    layer('opening')
    plane = rs.WorldXYPlane()
    rs.AddRectangle(plane, x, y)
    
    points=[]
    if num_hinges == 2:
        points.append([0,y*1/3,0])
        points.append([0,y*2/3,0])
        
    elif num_hinges == 3:
        points.append([0,y*1/4,0])
        points.append([0,y*2/4,0])
        points.append([0,y*3/4,0])
    
    return points

#add drawing geometry
def hinge(points=[0,0,0]):
    layer('hinge')
    
    for point in points:
        rs.InsertBlock('hinge', point)
def door(width, height, door_width, gasket_width=.25, channel_width=1):
    layer('door')
    plane = rs.WorldXYPlane()    
    #gasket_width, channel width
    gw, cw = gasket_width, channel_width
    
    #add door rectangle
    rs.AddRectangle(plane, door_width, height)
    #add gasket lines
    rs.AddLine([gw,gw*2,0],[gw,height,0])
    rs.AddLine([gw*2,gw*2,0],[gw*2,height,0])
    rs.AddLine([0,gw,0],[door_width,gw,0])
    rs.AddLine([0,gw*2,0],[door_width,gw*2,0])
    rs.AddLine([door_width-gw,cw,0],[door_width-gw,height,0])
    rs.AddLine([door_width+gw,cw,0],[door_width+gw,height,0])
    rs.AddLine([door_width-gw,cw,0],[door_width+gw,cw,0])
def side_light(width, height, door_width, channel_width=1):
    layer('side light')
    plane = rs.WorldXYPlane()
    cw = channel_width
    
    rs.AddRectangle(plane,door_width,height)
    rs.AddLine([door_width,cw,0],[width-cw,cw,0])
    rs.AddLine([width-cw,cw,0],[width-cw,height,0])    
def handle_elevation(door_width,handle_height=42):
    layer('handle')
    point = [door_width-6,handle_height,0]
    
    rs.InsertBlock('handle_elevation',point)
def handle_section(type):
    layer('handle_section')
    plane = rs.WorldXYPlane()
    
    point = [103,18,0]
    
    if str(type) == 'Round':
        rs.InsertBlock('handle_section_round',point)
        
    if str(type) == 'Square':
        rs.InsertBlock('handle_section_square',point)
    
def glass_streaks(width,height,door_width):
    layer('glass')
    
    rs.InsertBlock('glass_streak',[door_width/2,height/2,0])
    rs.InsertBlock('glass_streak',[door_width+(width-door_width)/2,height/2,0]) 
    
#add leaders
def leaders(list, width,height,door_width):
    layer('leaders')
    plane = rs.WorldXYPlane()
    
    points = [0,1,2,3,4,5] # create "empty" list indeces
    points.append([1,height/(num_hinges+1),0])#handle
    points.append([width,height-10,0])#uchannel
    points.append([door_width,height-15,0])#strike
    points.append([door_width/2,.25,0])#sill
    points.append([0.5,height*1/5,0])#door gasket
    points.append([door_width/3,height/2,0])#glass
    
    for i, note in enumerate(list):
        
        if i > 5 and i < 12:
            point1 = points[i]
            point2 = [points[i][0]-4,points[i][1]+3,0]
            point3 = [-5,points[i][1]+3,0]
            text = note[0]
            rs.AddLeader([point1,point2,point3],plane,text)
            
#add title block text and dims
def text_tb(list):
    layer('text')
    plane = rs.WorldXYPlane()
    
    #drawing title
    point1 = [174.778,-6.89789,0]
    text1 = str(list[0][0]) #omit first 3 characters with [2:] at the end
    rs.AddText(text1, point1, 1.5)
    
    #drawing number
    point2 = [174.868,-10.1477,0]
    text2 = 'XX-100'
    rs.AddText(text2, point2, 3)
    
    #date
    point3 = [183.13,36.7827,0]
    text3 = list[1][0]
    rs.AddText(text3, point3, .75)
    
def dimensions(width,height,door_width):
    layer('Dimensions')
    plane = rs.WorldXYPlane()
    
    point1 = [0,height,0]
    point2 = [width,height,0]
    point3 = [0,height+6,0]
    rs.AddAlignedDimension(point1,point2,point3)
    
    point4 = [0,0,0]
    point5 = [0,height,0]
    point6 = [-3,0,0]
    rs.AddAlignedDimension(point4,point5,point6)
    
    point7 = [0,height,0]
    point8 = [door_width,height,0]
    point9 = [0,height+3,0]
    rs.AddAlignedDimension(point7,point8,point9)

notes = import_notes('notes.csv')
leader = import_notes('checklist.csv')  
  
width = float(leader[2][0])
height = float(leader[3][0])
door_width = float(leader[4][0])
num_hinges = float(leader[5][0])

points = opening(width,height,num_hinges)
door(width,height,door_width)
hinge(points)
side_light(width,height,door_width)
handle_elevation(door_width)
handle_section(leader[12][0])
glass_streaks(width,height,door_width)
#NOTE - argument can't have the same name as function - i.e Leaders and Leaders
leaders(leader,width,height,door_width)
text_tb(leader)
dimensions(width,height,door_width)
