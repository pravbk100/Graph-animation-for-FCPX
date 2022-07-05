from tkinter import *
from tkinter import ttk, filedialog
import os, random, copy, pathlib, shutil
import xml.etree.ElementTree as ET
import numpy as np
from Bar_grapher import Bar_csv_process
from Bar_grapher_hor import Bar_hor_csv_process

main_path = pathlib.Path(__file__).resolve()
# mainXML_read = ET.parse(main_path.parent / 'line_graph_empty.motn').getroot()
# barXML_read = ET.parse(main_path.parent / 'bar_graph_empty.motn').getroot()
root = Tk()
root.title("Grapher for FCPX by PravBK")
root.iconbitmap(main_path.parent / 'picon.icns')
ws = int(root.winfo_screenwidth()/2)-200
hs = int(root.winfo_screenheight()/2)-200
root.geometry('400x300+'+str(ws)+'+'+str(hs))
frame = Frame(root)
frame.pack()

msg = StringVar()
msg.set('Please select the Options above. \n Then select your csv File.')
# var = IntVar()
menu_text, menu_text_b = StringVar(),StringVar()
menu_text.set('Row as Lines')
menu_text_b.set('Columns as Lines')

def retrieve_row_column():
	if vars2.get() == 0:
		btn.pack_forget()
	else:
		btn.pack(side = TOP, pady = 5)
		msg.set('Please select the Options above. \n Then select your csv File.')
	return vars2.get()

def retrieve_row_bar():
	if vars4.get() == 0:
		MenuBtt5.pack_forget()
		btn.pack_forget()
	else:
		MenuBtt5.pack(pady=5)
		msg.set('Please select the Options above. \n Then select your csv File.')
	return vars4

def retrieve_line_bar():
	if vars1.get() == 1:
		vars3.set(0)
		vars4.set(0)
		vars5.set(0)
		btn.pack_forget()
		MenuBtt2.pack(pady=5)
		MenuBtt3.pack_forget()
		MenuBtt4.pack_forget()
		MenuBtt5.pack_forget()
	elif vars1.get() == 2:
		vars2.set(0)
		btn.pack_forget()
		MenuBtt3.pack(pady=5)
		MenuBtt2.pack_forget()	
	else:
		btn.pack_forget()
		MenuBtt2.pack_forget()
		MenuBtt3.pack_forget()
		MenuBtt4.pack_forget()
		MenuBtt5.pack_forget()
		msg.set('Please select the Options above. \n Then select your csv File.')
	return vars1.get()

def retrieve_ver_hor():
	if vars3.get() == 0:
		MenuBtt4.pack_forget()
		btn.pack_forget()
	else:
		MenuBtt4.pack(pady=5)
		msg.set('Please select the Options above. \n Then select your csv File.')
	return vars3

def retrieve_onet():
	if vars5.get() == 0:
		btn.pack_forget()
	else:
		btn.pack(side = TOP, pady = 5)
		msg.set('Please select the Options above. \n Then select your csv File.')
	return vars5.get()

MenuBtt1 = ttk.Menubutton(frame, text = "Graph Type")
vars1 = IntVar()
Menu1 = Menu(MenuBtt1, tearoff = 0)
Menu1.add_checkbutton(label = "Line graph", variable = vars1, onvalue=1, offvalue=0,command = retrieve_line_bar)
Menu1.add_checkbutton(label = "Bar graph", variable = vars1, onvalue=2, offvalue=0,command = retrieve_line_bar)
MenuBtt1["menu"] = Menu1
MenuBtt1.pack(pady=10)

MenuBtt2 = ttk.Menubutton(frame, text = "Select")
vars2, vars3, vars4, vars5 = IntVar(),IntVar(),IntVar(),IntVar()
Menu2 = Menu(MenuBtt2, tearoff = 0)
Menu2.add_checkbutton(label = 'Rows as Lines', variable = vars2, onvalue=1, offvalue=0,command = retrieve_row_column)
Menu2.add_checkbutton(label = 'Columns as Lines', variable = vars2, onvalue=2, offvalue=0,command = retrieve_row_column)
MenuBtt2["menu"] = Menu2

MenuBtt3 = ttk.Menubutton(frame, text = "Select")
Menu3 = Menu(MenuBtt3, tearoff = 0)
Menu3.add_checkbutton(label = 'Horizontal Bars', variable = vars3, onvalue=1, offvalue=0,command = retrieve_ver_hor)
Menu3.add_checkbutton(label = 'Vertical Bars', variable = vars3, onvalue=2, offvalue=0,command = retrieve_ver_hor)
MenuBtt3["menu"] = Menu3

MenuBtt4 = ttk.Menubutton(frame, text = "Select")
Menu4 = Menu(MenuBtt4, tearoff = 0)
Menu4.add_checkbutton(label = 'Rows as Bars', variable = vars4, onvalue=1, offvalue=0,command = retrieve_row_bar)
Menu4.add_checkbutton(label = 'Columns as Bars', variable = vars4, onvalue=2, offvalue=0,command = retrieve_row_bar)
MenuBtt4["menu"] = Menu4

MenuBtt5 = ttk.Menubutton(frame, text = "Select")
Menu5 = Menu(MenuBtt5, tearoff = 0)
Menu5.add_checkbutton(label = 'One time Animation', variable = vars5, onvalue=1, offvalue=0,command = retrieve_onet)
Menu5.add_checkbutton(label = 'Continuous Animation', variable = vars5, onvalue=2, offvalue=0,command = retrieve_onet)
MenuBtt5["menu"] = Menu5

btn = Button(root, text ='Select the csv file',bg="red", fg="black", width = '19', command = lambda:open_file())

processing = Label(root,textvariable= msg,foreground='green')
processing.pack(side = TOP, pady = 5)

def open_file():
	try:
		csv_path_file = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = [('csv Files', '*.csv')])
		if csv_path_file is not None and vars1.get() == 1:
			mainXML_read = ET.parse(main_path.parent / 'line_graph_empty.motn').getroot()
			write_off(csv_process(csv_path_file,mainXML_read,vars2.get()),csv_path_file,vars1.get())
		elif csv_path_file is not None and vars1.get() == 2 and vars3.get() == 1:
			barXML_read = ET.parse(main_path.parent / 'bar_empty_horizontal.motn').getroot()
			write_off(Bar_hor_csv_process(csv_path_file,barXML_read,vars3.get(),vars4.get(),vars5.get()),csv_path_file,vars1.get())
		elif csv_path_file is not None and vars1.get() == 2 and vars3.get() == 2:
			barXML_read = ET.parse(main_path.parent / 'bar_graph_empty.motn').getroot()
			write_off(Bar_csv_process(csv_path_file,barXML_read,vars3.get(),vars4.get(),vars5.get()),csv_path_file,vars1.get())		
		else:
			msg.set('No File Selected')
	except:
		msg.set('Something went wrong')
  
def csv_process(in_csv,mainXML_read,retrieve_row_column):
	try:
		csv = np.genfromtxt(in_csv, dtype=str, delimiter=",")
		csv = csv.T if retrieve_row_column == 2 else csv
		column_deviders = csv[0][1:]########## columns for x axis texts and values ############
		# print(column_deviders)
		line_names = [x[0] for x in csv[1:]]################ number of lines and names ############
		lines_and_values = np.asarray([x[1:] for x in csv[1:]]).astype("float")############ pixel values list for graph  ############
		yText_list = np.round(np.linspace(lines_and_values.min(), lines_and_values.max(), num=5)).astype("str") #------
		xRange = len(column_deviders) if len(column_deviders) < 15 else 5
		xText_list = [column_deviders[x] for x in np.round(np.linspace(0,len(column_deviders)-1, num=xRange)).astype('int')] 
		xText_Pixel = np.round(np.linspace(0, 3500, num=xRange)).astype("int").astype("str") #------
		yText_Pixel = np.linspace(0, 2000, num=5).astype("str") #------
		yPoint_values = np.interp(lines_and_values, (lines_and_values.min(), lines_and_values.max()), (0, 2000)).astype("str")
		xPoint_values = np.linspace(0, 3500, num=len(yPoint_values[0])).astype("str")
		return gotoxml(mainXML_read,line_names,yText_list,xText_list,xText_Pixel,yText_Pixel,yPoint_values,xPoint_values,xRange,in_csv)
	except:
		msg.set('Cant process csv')

def gotoxml(mainXMLl,line_names,yText_list,xText_list,xText_Pixel,yText_Pixel,yPoint_values,xPoint_values,xRange,in_csv):
	mainXML = copy.deepcopy(mainXMLl)
	layerids = []
	#### random integer gen function ############
	def randLayerIdGen():
		a = str(random.choice([x for x in range(100800,300400) if x not in layerids]))
		layerids.append(a)
		return a
	#### random integer gen function ##########\\

	#### position function ############
	def Positionshift():
		for i in mainXML.iter('parameter'):
			if i.attrib['name'] == 'Position':
				for x in i.iter('parameter'):
					if x.attrib['name'] == 'X':
						x.attrib['value'] = str(200)
	#### position function ##########\\

	###### mainXML set variables and cleanUp ###########
	main_gp = mainXML.find('./scene/layer[@name="Main_Group"]')###### set main group layer variable
	pubset = mainXML.find('./scene/publishSettings')[-1]###### set publish setting variable
	oneline = mainXML.find("./scene/layer/scenenode[@name='Line0']")###### set line variable
	vertex = oneline.find('.//vertex[@flags="8"]') ####### set vertex variable
	oneline.find('./parameter/parameter/parameter/curve_X').remove(vertex)###### vertex remove
	oneline.find('./parameter/parameter/parameter/curve_Y').remove(oneline.find('./parameter/parameter/parameter/curve_Y/vertex'))###### vertex remove
	layernames = [x.attrib['name'] for x in main_gp.findall('./scenenode') if isinstance(x.attrib['name'][-1], int)]####### set layer names list
	layerids = [x.attrib['id'] for x in main_gp.findall('./scenenode')]####### set layer ids list
	layerFids = [x.attrib['factoryID'] for x in main_gp.findall('./scenenode')]####### set layer factoryIds list
	main_gp.remove(oneline)###### remove line
	mainXML.find('./scene/publishSettings').remove(mainXML.find('./scene/publishSettings')[-1])###### remove publish setting of line
	text_gp = mainXML.find('./scene/layer/layer[@name="Text_Group"]')###### set text group layer variable
	textLayer = mainXML.find('./scene/layer/layer[@name="Text_Group"]/scenenode[@name="pGraph0"]')###### set text layer variable
	textlayerNames = [x.attrib['name'] for x in text_gp.findall('./scenenode') if isinstance(x.attrib['name'][-1], int)]
	text_gp.remove(textLayer)
	mainXML.find('.//scenenode/parameter/parameter/parameter[@name="Points"]').attrib['value'] = str(xRange)
	colT_gp = mainXML.find('./scene/layer/layer[@name="Col_Text_Group"]')
	colT_sub_gp = colT_gp.find('./group[@name="CTgp0"]')
	colT_gp.remove(colT_sub_gp)
	###### mainXML set variables and cleanUp ##########\\

	###### insert line etxt group function ###########
	def coltinsert(ypos,textVal,colLink):
		colText_gp = copy.deepcopy(colT_sub_gp)
		colText_gp.attrib['id'] = randLayerIdGen()
		colText_gp.attrib['name'] = textVal + ' Gp'
		textLayer = colText_gp.find('./scenenode[@factoryID="22"]')
		textLayer.attrib['id'] = randLayerIdGen()
		textLayer.attrib['name'] = textVal
		textLayer.find('.//text').text = textVal
		textLayer.find('.//parameter[@name="Position"]//parameter[@name="Y"]').attrib['value'] = str(ypos)
		RectLayer = colText_gp.find('./scenenode[@factoryID="16"]')
		# RectLayer.attrib['name'] = textLayer.attrib['name'] + ' R'
		RectLayer.attrib['id'] = randLayerIdGen()
		RectLayer.attrib['name'] = textLayer.attrib['name'] + 'R'
		RectLayer.find('.//behavior[@name="Link"]/parameter[@name="Source Object"]').attrib['value'] = colLink
		RectLayer.find('./behavior[@name="Align To"]/parameter[@name="Object"]').attrib['value'] = textLayer.attrib['id']
		return colText_gp
	###### insert line etxt group function #########\\

	###### vertex set function ###########
	def insertvertex(v_index,v_id,v_val):
		vert = copy.deepcopy(vertex)
		vert.attrib['index'] = v_index
		vert.attrib['id'] = v_id
		vert[0].attrib['id'] = v_id
		vert[0][0].attrib['value'] = v_val
		return vert
	###### vertex set function ##########\\

	###### textlayer set function ###########
	def insertText(in_text,in_XTvalue,in_YTvalue,align):
		textL = copy.deepcopy(textLayer)
		textL.attrib['name'] = in_text
		textL.attrib['id'] = randLayerIdGen()
		textL.find('.//text').text = in_text
		textL.find('.//parameter[@name="X"]').attrib['value'] = in_XTvalue
		textL.find('.//parameter[@name="Y"]').attrib['value'] = in_YTvalue
		textL.find('./parameter//parameter[@name = "Alignment"]').attrib['value'] = align
		return textL
	###### textlayer set function #########\\

	###### insert all function ###########
	def insertLine(inXtext,inXtext_v,inYtext,inYtext_v,vX_Points,vY_Points,l_index):
		aline = copy.deepcopy(oneline)
		# aline.attrib['name'] = aline.attrib['name'][:-1] + str(int(layernames[-1][-1])+1) if aline.attrib['name'] in layernames else aline.attrib['name']
		# layernames.append(aline.attrib['name'])
		aline.attrib['name'] = str(line_names[l_index])
		aline.attrib['id'] = randLayerIdGen()
		aline.find('.//parameter[@name="Red"]').attrib['value'] = str(random.random())
		aline.find('.//parameter[@name="Green"]').attrib['value'] = str(random.random())
		aline.find('.//parameter[@name="Blue"]').attrib['value'] = str(random.random())

		###### behavior, publish settings ###########
		new_pubsetting = copy.deepcopy(pubset)
		for i in aline.findall('.//parameter[@name="Affecting Object (Hidden)"]'):
			i.attrib['value'] = aline.attrib['id']
		new_pubsetting.attrib['object'] = aline.attrib['id']
		new_pubsetting.attrib['name'] = aline.attrib['name']
		###### behavior, publish settings #########\\

		###### add vertex ###########
		for i in range(len(vY_Points)):
			vid = 15
			xv_value,yv_value = vX_Points[i], vY_Points[i]
			vert_x = insertvertex(str(i),str(vid),str(xv_value))
			aline.find('.//curve_X').append(vert_x)
			vert_y = insertvertex(str(i),str(vid+1),str(yv_value))
			aline.find('.//curve_Y').append(vert_y)
			vid+=2
		###### add vertex #########\\
		if l_index == 0:
			for i in range(len(inXtext)):
				text_gp.append(insertText(inXtext[i],inXtext_v[i],'-250','1'))
			for i in range(len(inYtext)):
				text_gp.append(insertText(inYtext[i],'-250',inYtext_v[i],'2'))

		colT_gp.append(coltinsert(l_index*(-150),str(line_names[l_index]),aline.attrib['id']))

		main_gp.insert(0,aline)
		mainXML.find('./scene/publishSettings').append(new_pubsetting)
	###### insert all function #########\\

	for i in range(len(yPoint_values)):
		if len(yPoint_values) < 10:
			# print(mainXML)
			insertLine(xText_list,xText_Pixel,yText_list,yText_Pixel,xPoint_values,yPoint_values[i],i)
		else:
			msg.set('10 Lines max Allowed.\n Please Use Different Row/Column setting')
	
	return [mainXML, '0']

def write_off(mainL,in_csv,line_or_bar):
	# print(mainL[1])
	# print(mainL[0])
	foldername = 'lineGraph_template'
	filename = 'linegraph'
	if mainL == 'Cant process':
		msg.set('Cant process')
	else:
		if line_or_bar == 1:
			foldername = 'lineGraph_template'
			filename = 'linegraph'
		else:
			foldername = 'barGraph_template'
			filename = 'bargraph'

		smIm_path = main_path.parent / 'small.png'
		laIm_path = main_path.parent / 'large.png'

		if os.path.isdir(in_csv.rsplit('/', 1)[0] + '/'+ foldername):
			msg.set('Template folder already exists.')
		else:
			path = in_csv.rsplit('/', 1)[0] + '/' + foldername
			os.mkdir(path)
			media_f = path + '/Media'
			os.mkdir(media_f)
			line_grapher = os.path.abspath('line_grapher')
			shutil.copy(smIm_path,path)
			shutil.copy(laIm_path,path)

			if not isinstance(mainL[1], str):
				with open(media_f+'/'+'a.txt', 'w') as ff:
					for i in mainL[1]:
						ff.write(str(i) + '\n')

			md = ET.tostring(mainL[0])
			with open(path+'/'+ filename+'.motn','wb') as f:
				f.write(md)
			msg.set('Hooray, Its Done. \n Template folder created in your csv file path.')
			### save file #########\\

mainloop()