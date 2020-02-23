from django.shortcuts import render
from django.http import HttpResponse

import pyodbc

conn = pyodbc.connect(
	"Driver={SQL Server Native Client 11.0};"
	"Server=LAPTOP-EQJLRAGV\\SQLEXPRESS;"
	"Database=project;"
	"Trusted_Connection=yes"
	)
conn1 = pyodbc.connect(
	"Driver={SQL Server Native Client 11.0};"
	"Server=LAPTOP-EQJLRAGV\\SQLEXPRESS;"
	"Database=project;"
	"Trusted_Connection=yes"
	)



def read(conn,strs):
	
	cursor = conn.cursor()
	cursor.execute(strs)
	return cursor

def insert(conn,strs):
	cursor = conn.cursor()
	cursor.execute(strs)
	conn.commit()

def index(request):
	con = read(conn,"Select Changes.change_id,Cars.mark, Changes.type_of_change,Changes.change_date,Changes.maxspeed_change,Changes.power_change,Details.name,Details.detail_price,Details.guarantee FROM Changes JOIN Cars ON Cars.car_id=Changes.car_id JOIN Details On Details.detail_id=Changes.detail_id")
	lis2 = []
	c = read(conn1,'select car_id,mark,max_speed,power from Cars')

	for i in c:
		dic = {
			'car_id':i[0],
			'mark':i[1],
			'max_speed':i[2],
			'power':i[3]
		}
		lis2.append(dic)
	changes = []
	details=  []
	price = []
	lis= []
	for i in con:
		dic  = {
			'id':i[0],
			'mark':i[1],
			'type_of_change':i[2],
			'change_date':i[3],
			'maxspeed_change':i[4],
			'power_change':i[5],
			'detail_name':i[6],
			'detail_price':i[7],
			'detail_guarantee':i[8]
		}
		if i[2] not in changes:
			changes.append(i[2])
		if i[6] not in details:
			details.append(i[6])
			di = {
				'detail_name':i[6],
				'detail_price':i[7]
			}
			price.append(di)
		lis.append(dic)

	
	context = {"rows":lis,'changes':changes,'details':details,'cars':lis2,'price':price}

	
	
	return render(request,'main/index.html',context)


def staff(request):
	lis = []
	lis2 = []
	if (request.method=='POST'):
		con = read(conn,"Select Employees.employee_id,Employees.first_name,Employees.last_name,Autotune.autotune_name,Employees.hire_date,Position.Position_name,Position.Salary,Cities.city_name FROM Employees JOIN Autotune ON Autotune.autotune_id=Employees.autotune_id JOIN Position ON Position.Position_id=Employees.Position_id JOIN Cities ON Cities.city_id=Autotune.city_id WHERE "+request.POST.get('search')+"='"+request.POST.get('searchby')+"'")
		for i in con:
			dic  = {
				'id': i[0],
				'first_name':i[1],
				'last_name':i[2],
				'autotune_name':i[3],
				'hire_date':i[4],
				'position_name':i[5],
				'salary':i[6],
				'city':i[7]
			}
			lis2.append(dic)


	con = read(conn,"Select Employees.employee_id,Employees.first_name,Employees.last_name,Autotune.autotune_name,Employees.hire_date,Position.Position_name,Position.Salary,Cities.city_name FROM Employees JOIN Autotune ON Autotune.autotune_id=Employees.autotune_id JOIN Position ON Position.Position_id=Employees.Position_id JOIN Cities ON Cities.city_id=Autotune.city_id")
	for i in con:

		dic  = {
			'id':i[0],
			'first_name':i[1],
			'last_name':i[2],
			'autotune_name':i[3],
			'hire_date':i[4],
			'position_name':i[5],
			'salary':i[6],
			'city':i[7]
		}
		lis.append(dic)
			
	context = {"rows":lis,'emps':lis2}
	return render(request,'main/staff.html',context)

def cars(request):

	lis = []
	if (request.method == "POST" and request.POST.get('submit')):
		insert(conn,"Insert INTO [Owner] (owner_id,name,surname) VALUES ({0},'{1}','{2}');INSERT INTO Cars (car_id,owner_id,color,[power],release_date,mark,max_speed) VALUES ({3},{4},'{5}','{6}',{7},'{8}','{9}')".format(request.POST.get('owner_id'),request.POST.get('name'),request.POST.get('surname'),request.POST.get('car_id'),request.POST.get('owner_id'),request.POST.get('color'),request.POST.get('power'),request.POST.get('release_date'),request.POST.get('mark'),request.POST.get('max_speed')))
	if(request.method == "POST" and len(str(request.POST.get('car')))!=0):
		try:
			con = read(conn,"Select Owner.name,Owner.surname,Cars.mark,Cars.color,Cars.power,Cars.max_speed,Cars.release_date FROM Cars JOIN Owner ON Owner.owner_id=Cars.owner_id WHERE Cars.mark='"+str(request.POST.get('car'))+"' Order BY " +request.POST.get(
				"order"))
		except Exception:
			
			con = read(conn,"Select Owner.name,Owner.surname,Cars.mark,Cars.color,Cars.power,Cars.max_speed,Cars.release_date FROM Cars JOIN Owner ON Owner.owner_id=Cars.owner_id WHERE Cars.mark='"+str(request.POST.get('car'))+"'")
		for i in con:
			dic  = {
			'name':i[0],
			'surname':i[1],
			'mark':i[2],
			'color':i[3],
			'power':i[4],
			'max_speed':i[5],
			'release_date':i[6],
	}	
			lis.append(dic)
	else:
		con = read(conn,"Select Owner.name,Owner.surname,Cars.mark,Cars.color,Cars.power,Cars.max_speed,Cars.release_date FROM Cars JOIN Owner ON Owner.owner_id=Cars.owner_id")

		for i in con:
			dic  = {
			'name':i[0],
			'surname':i[1],
			'mark':i[2],
			'color':i[3],
			'power':i[4],
			'max_speed':i[5],
			'release_date':i[6],
			}	
			lis.append(dic)
	context = {"rows":lis}
	
	return render(request,'main/cars.html',context)


def change_info(request,id):

	con = read(conn,"Select Cars.mark, Changes.type_of_change,Changes.change_date,Changes.maxspeed_change,Changes.power_change,Details.name,Details.detail_price,Details.guarantee,Employees.first_name,Employees.last_name,Autotune.autotune_name,Cities.city_name,Countries.country_name,Details.guarantee FROM Changes JOIN Cars ON Cars.car_id=Changes.car_id JOIN Details On Details.detail_id=Changes.detail_id JOIN Employees ON Employees.employee_id=Changes.mechanic_id JOIN Autotune ON Autotune.autotune_id=Employees.autotune_id JOIN Cities ON Cities.city_id=Autotune.city_id JOIN Countries ON Countries.country_id=Cities.country_id WHERE Changes.change_id="+str(id))
	
	lis= []
	for i in con:
		dic  = {
			'mark':i[0].strip(),
			'type_of_change':i[1].strip(),
			'change_date':i[2],
			'maxspeed_change':i[3],
			'power_change':i[4],
			'detail_name':i[5].strip(),
			'detail_price':i[6],
			'detail_guarantee':i[7],
			'fname':i[8].strip(),
			'lname':i[9].strip(),
			'autotune_name':i[10].strip(),
			'city':i[11].strip(),
			'country':i[12].strip(),
			'guarantee':i[13]
		}
		lis.append(dic)
	context = {'info':lis}
	return render(request,'main/change_info.html',context)

def staff_info(request,id):
	
	return render(request,'main/staff_info.html')