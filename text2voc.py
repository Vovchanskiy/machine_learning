import urllib.request
from PIL import Image
import PIL
import math

raw_file = open('/Users/kalinin/downloads/cigarettes/raw_annotations/gistfile1.txt', 'r')

start_img = '{"id":'
end_img = ']}]}'
start_http = 'http:'
end_http = 'imgs'
start_points = 'points":['
end_points = ']}'
start_pionts_x = 'x":'
end_points_x = ','
start_pionts_y = 'y":'
end_points_y = '}'


for line in raw_file:
	start_index_img = 0
	object_total = 0
	not_object_total = 0
	for i in range(line.count(start_img)):
		#определение аннотаций для одной картинки
		start_index = line.find(start_img, start_index_img)
		end_index = line.find(end_img, start_index_img)+len(end_img)
		img = line[start_index:end_index]
		start_index_img = end_index

		#поиск ссылки на картинку
		start_index = line.find(start_http, start_index)
		end_index = line.find(end_http, start_index)-3
		img_http = line[start_index:end_index]

		#имя картинки
		start_index = img_http.rfind('/')+1
		end_index = img_http.rfind('.')
		http_name = img_http[start_index:end_index]

		#скачивание картинки
		urllib.request.urlretrieve(img_http, '/Users/kalinin/downloads/cigarettes/JPEGImages/'+http_name+'.jpg')

		im = Image.open('/Users/kalinin/downloads/cigarettes/JPEGImages/'+http_name+'.jpg')
		width, height = im.size

		#изменение размера изображения с сохранением пропорций
		if width>height:
			wsize = 500
			wpercent = (wsize/float(width))
			hsize = int((float(height)*float(wpercent)))
			im = im.resize((wsize,hsize), PIL.Image.ANTIALIAS)
		else:
			hsize = 500
			hpercent = (hsize/float(height))
			wsize = int((float(width)*float(hpercent)))
			im = im.resize((wsize,hsize), PIL.Image.ANTIALIAS)

		im.save('/Users/kalinin/downloads/cigarettes/JPEGImages/'+http_name+'.jpg')
		im.close()

		with open('/Users/kalinin/downloads/cigarettes/Annotations/'+http_name+'.xml', 'w') as f:
			line_xml = '<annotation>' + '\n'
			f.write(line_xml)
			line_xml = '\t<folder>' + 'Cigarettes' + '</folder>' + '\n'
			f.write(line_xml)
			line_xml = '\t<filename>' + http_name+'.jpg' + '</filename>' + '\n'
			f.write(line_xml)
			line_xml = '\t<size>' + '\n'
			f.write(line_xml)
			line_xml = '\t\t<width>' + str(wsize) + '</width>' + '\n'
			f.write(line_xml)
			line_xml = '\t\t<height>' + str(hsize) + '</height>' + '\n'
			f.write(line_xml)
			line_xml = '\t\t<depth>' + str(3) + '</depth>' + '\n'
			f.write(line_xml)
			line_xml = '\t</size>' + '\n'
			f.write(line_xml)

		start_index_box = 0
		not_object_count = 0
		object_count = img.count('points')
		for j in range(img.count('points')):

			#поиск координат bounding boxes
			start_index = img.find(start_points, start_index_box)+len(start_points)
			end_index = img.find(end_points, start_index)#+len(end_points)
			img_points = img[start_index:end_index]
			start_index_box = end_index

			#поиск четырех координат бокса
			start_index_points = 0
			points_x = []
			points_y = []
			for k in range(img_points.count('x')):
				#поиск икса
				start_index = img_points.find(start_pionts_x, start_index_points)+len(start_pionts_x)
				end_index = img_points.find(end_points_x, start_index_points)
				img_points_x = img_points[start_index:end_index]
				#поиск игрека
				start_index = img_points.find(start_pionts_y, start_index_points)+len(start_pionts_y)
				end_index = img_points.find(end_points_y, start_index_points)
				img_points_y = img_points[start_index:end_index]
				start_index_points = end_index + 2
				points_x.append(img_points_x)
				points_y.append(img_points_y)

			#координаты прямоугольника bounding box
			x_min = math.floor( float(min(points_x))*(wsize/float(width)) )
			x_max = math.floor( float(max(points_x))*(wsize/float(width)) )
			y_min = math.floor( float(min(points_y))*(hsize/float(height)) )
			y_max = math.floor( float(max(points_y))*(hsize/float(height)) )
			
			#исключение невилидных боксов
			not_object = 0
			if int(y_max) > hsize and int(y_max) > wsize:
				not_object = 1
			if int(x_max) > hsize and int(x_max) > wsize:
				not_object = 1
			# if int(y_max) == int(y_min):
			# 	not_object = 1
			# if int(x_max) == int(x_min):
			# 	not_object = 1
			if int(y_max)-int(y_min)<2:
				not_object = 1
			if int(x_max)-int(x_min)<2:
				not_object = 1
			#x - это width
			if int(y_max) == hsize:
				y_max = int(y_max)-1
			if int(x_max) == wsize:
				x_max = int(x_max)-1
			if int(y_min) == 0:
				y_min = int(y_min)+1
			if int(x_min) == 0:
				x_min = int(x_min)+1

			if not_object == 0:
				with open('/Users/kalinin/downloads/cigarettes/Annotations/'+http_name+'.xml', 'a') as f:
					line_xml = '\t<object>' + '\n'
					f.write(line_xml)
					line_xml = '\t\t<name>' + 'cigarettes' + '</name>' + '\n'
					f.write(line_xml)
					line_xml = '\t\t<bndbox>' + '\n'
					f.write(line_xml)
					line_xml = '\t\t\t<xmin>' + str(x_min) + '</xmin>' + '\n'
					f.write(line_xml)
					line_xml = '\t\t\t<ymin>' + str(y_min) + '</ymin>' + '\n'
					f.write(line_xml)
					line_xml = '\t\t\t<xmax>' + str(x_max) + '</xmax>' + '\n'
					f.write(line_xml)
					line_xml = '\t\t\t<ymax>' + str(y_max) + '</ymax>' + '\n'
					f.write(line_xml)
					line_xml = '\t\t</bndbox>' + '\n'
					f.write(line_xml)
					line_xml = '\t</object>' + '\n'
					f.write(line_xml)
			else:
				not_object_count += 1

		with open('/Users/kalinin/downloads/cigarettes/Annotations/'+http_name+'.xml', 'a') as f:
			line_xml = '</annotation>' + '\n'
			f.write(line_xml)

		print(str(i+1) + '/' + str(line.count(start_img)) + ' число объектов: ' + str(img.count('points')) + ', число исключенных объектов: ' + str(not_object_count))
		object_total += object_count
		not_object_total += not_object_count

	img_count = line.count(start_img)
	print('всего картинок:', img_count)
	print('всего объектов:', object_total)
	print('всего исключено объектов:', not_object_total)

