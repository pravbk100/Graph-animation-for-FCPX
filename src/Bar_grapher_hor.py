import os, random, copy, pathlib, shutil
import xml.etree.ElementTree as ET
import numpy as np
 
def Bar_hor_csv_process(in_csv,barXML_read,ver_hor,row_col,onet):
	try:
		csv = np.genfromtxt(in_csv, dtype=str, delimiter=",")
		csv = csv.T if row_col == 2 else csv #1 for column 0 for rows
		column_deviders = csv[0][1:]########## columns for x axis texts and values ############
		bar_names = [x[0] for x in csv[1:]]################ number of lines and names ############
		lines_and_values = np.asarray([x[1:] for x in csv[1:]]).astype("float")############ pixel values list for graph  ############
		# print(bar_names)
		yText_list = np.round(np.linspace(lines_and_values.min(), lines_and_values.max(), num=5)).astype("str") #------
		xRange = len(column_deviders) if len(column_deviders) < 15 else 5
		xText_list = [column_deviders[x] for x in np.round(np.linspace(0,len(column_deviders)-1, num=xRange)).astype('int')] 
		xText_Pixel = np.round(np.linspace(0, 2000, num=xRange)).astype("int").astype("str") #------
		yText_Pixel = np.linspace(0, 3400, num=5).astype("str") #------
		yPoint_values = np.interp(lines_and_values, (lines_and_values.min(), lines_and_values.max()), (0, 3400))
		xPoint_values = np.linspace(0, 2000, num=len(yPoint_values[0])).astype("str")
		if len(bar_names) < 15:
			return gotoxml(barXML_read,bar_names,yText_list,yText_Pixel,lines_and_values,yPoint_values,onet,column_deviders)
		else:
			return 'Cant process'
	except:
		return 'Cant process'

#### random integer gen function ############
layerids = []
def randLayerIdGen():
	a = str(random.choice([x for x in range(200800,300400) if x not in layerids]))
	layerids.append(a)
	return a
#### random integer gen function ##########\\

def gotoxml(mainXMLl,bar_names,yText_list,yText_Pixel,lines_values,yPoint_values,onetime_ani,column_deviders):
	mainXML = copy.deepcopy(mainXMLl)
	main_gp = mainXML.find('./scene/layer[@name="Main_Group"]')
	bar_gp = mainXML.find('./scene/layer/group[@name="Bar_gp"]')###### set main group layer variable
	pubset_pos = mainXML.find('./scene/publishSettings/target[@object="101989"]')###### set publish setting variable
	pubset_col = mainXML.find('./scene/publishSettings/target[@object="101964"]')###### set publish setting variable
	main_gp.remove(bar_gp)
	mainXML.find('./scene/publishSettings').remove(pubset_pos)
	mainXML.find('./scene/publishSettings').remove(pubset_col)

	bar_text_b = main_gp[1]
	main_gp.remove(bar_text_b)
	def add_bar_b(main_gp,bar_text_b,yText_list,yText_Pixel):
		bar_text_b = copy.deepcopy(bar_text_b)
		bar_text_b.attrib['id'] = randLayerIdGen()
		bar_text_b.attrib['name'] = yText_list
		bar_text_b.find('.//text').text = yText_list
		bar_text_b.find('.//parameter[@name="X"]').attrib['value'] = yText_Pixel
		# print(bar_text_b.find('.//text').text)
		return bar_text_b
	for i in range(0,len(yText_list)):
		main_gp.insert(1, add_bar_b(main_gp,bar_text_b,yText_list[i],yText_Pixel[i]))

	xpos = 1900/len(bar_names)
	for i in range(0, len(bar_names)):
		add_bar(mainXML,main_gp,bar_gp,bar_names[i],lines_values[i],yPoint_values[i],pubset_pos,pubset_col,str(xpos),onetime_ani)
		xpos += 1900/len(bar_names)
		# break
		
	if onetime_ani == 1:
		mainXML.find('./scene/layer[@name="atextgp"]').remove(mainXML.find('./scene/layer[@name="atextgp"]/scenenode[@name="File"]'))
		return [mainXML, '0']
	else:
		text_gen_layer = mainXML.find('./scene/layer[@name="atextgp"]/scenenode[@name="File"]')
		text_gen_layer[0].text = 'Media/a.txt'
		text_gen_layer.find('./timing').attrib['in'] = str(5120*int(301/len(column_deviders))) + ' ' + '153600' + ' ' + '1' + ' ' + '0'
		return [mainXML, column_deviders]

def add_bar(mainXML,main_gp,bar_gp,bar_names,line_vals,yPoint_values,pubset_pos,pubset_col,xpos,onetime_ani):
	bar_gp = copy.deepcopy(bar_gp)
	bar_gp.attrib['id'] = randLayerIdGen()
	bar_gp.attrib['name'] = bar_names + '_gp'
	bar_gp.find('./parameter/parameter/parameter/parameter[@name="Y"]').attrib['value'] = xpos
	pubset_pos = copy.deepcopy(pubset_pos)
	pubset_pos.attrib['object'] = bar_gp.attrib['id']
	pubset_pos.attrib['name'] = bar_gp.attrib['name'][:-3] + ' Position'
	bar = bar_gp[1]
	bar.attrib['id'] = randLayerIdGen()
	bar.attrib['name'] = bar_gp.attrib['name'][:-3] + ' Bar'
	curve = bar.find('./parameter/parameter/parameter/parameter/curve')
	keypoint = bar.find('./parameter/parameter/parameter/parameter/curve')[1]
	keypoint_end = bar.find('./parameter/parameter/parameter/parameter/curve')[2]
	curve.remove(keypoint_end)

	numbers = bar_gp[0]
	numbers.attrib['id'] = randLayerIdGen()
	numbers.attrib['name'] = bar_gp.attrib['name'][:-3] + ' Numbers'	
	numbers.find('./behavior[@name="Align To"]/parameter[@name="Object"]').attrib['value'] = bar.attrib['id']
	for_decimal = [(lambda x:len(x.split('.')[1]))(str(x)) for x in line_vals]
	numbers.find('./parameter/parameter/parameter[@name="Decimals"]').attrib['value'] = str(max(for_decimal)) if max(for_decimal) <= 3 else '2'
	num_curve = numbers.find('./parameter/parameter/parameter[@name="Value"]/curve')
	num_keypoint = numbers.find('./parameter/parameter/parameter[@name="Value"]/curve')[1]
	num_keypoint_end = numbers.find('./parameter/parameter/parameter[@name="Value"]/curve')[2]
	num_curve.remove(num_keypoint_end)
	# num_curve.remove(num_keypoint)

	def add_key(curve,keypoint,pval,time_gap,yP_value,num_curve,num_keypoint,lin_val):
		keypoint = copy.deepcopy(keypoint)
		num_keypoint = copy.deepcopy(num_keypoint)
		keypoint[0].text = str(pval*(time_gap)) + ' ' + '153600' + ' ' + '1' + ' ' + '0'
		keypoint[1].text = str(yP_value)
		num_keypoint[0].text = keypoint[0].text
		num_keypoint[1].text = str(lin_val)
		curve.append(keypoint)
		num_curve.append(num_keypoint)

	pval = 5120
	if onetime_ani == 1:
		num_keypoint[1].text = str(line_vals.min())
		add_key(curve,keypoint,pval*299,1,yPoint_values.max(),num_curve,num_keypoint,line_vals.max())
	else:
		num_keypoint[1].text = str(random.randint(200,3000))
		for i in range(0,len(yPoint_values)): 
			time_gap = int(301/len(yPoint_values))
			add_key(curve,keypoint,pval,time_gap,yPoint_values[i],num_curve,num_keypoint,line_vals[i])
			pval += 5120
			# break

	bar_text = bar_gp[2]
	bar_text.attrib['id'] = randLayerIdGen()
	bar_text.attrib['name'] = bar_gp.attrib['name'][:-3] + ' Text'
	bar_text.find('.//text').text = bar_gp.attrib['name']

	pubset_col = copy.deepcopy(pubset_col)
	pubset_col.attrib['object'] = bar.attrib['id']
	pubset_col.attrib['name'] = bar.attrib['name'] + ' Color'
	main_gp.insert(1,bar_gp)
	mainXML.find('./scene/publishSettings').append(pubset_pos)
	mainXML.find('./scene/publishSettings').append(pubset_col)
	# return mainXML
	# md = ET.tostring(mainXML)
	# with open('bgGraph.motn','wb') as f:
	# 	f.write(md)

	
