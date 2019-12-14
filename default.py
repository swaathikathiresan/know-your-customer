from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config,notfound_view_config

from sqlalchemy.exc import DBAPIError
from sqlalchemy import and_
from pyramid_sqlalchemy import Session

from ..models import MyModel
from ..models import Houseowner,Vehicle,Tenant,User_Admin
from pyramid.session import SignedCookieSessionFactory



# @view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
# def my_view(request):
#     try:
#         query = request.dbsession.query(MyModel)
#         one = query.filter(MyModel.name == 'one').first()
#     except DBAPIError:
#         return Response(db_err_msg, content_type='text/plain', status=500)
#     return {'one': one, 'project': 'agrini'}
#ok

@view_config(route_name='addhouseownerpg', renderer='../templates/houseowner.jinja2')
def addhouseownerpg(request):
    try:
        if request.session['role']=='admin':
            if request.method=='POST':
                obj=Houseowner()
                obj.houseownername =request.params['houseownername']
                obj.username =request.params['username']
                obj.password=request.params['password']
                # request.session['houseownername']=request.params['houseownername']

                obj.fathername=request.params['fathername']
                obj.permanentaddress =request.params['address']
                obj.contactmobileno=request.params['ph_no']
                obj.landline_no=request.params['landline_no']
                obj.emailid=request.params['email']
                obj.emergencycontactname=request.params['emername']
                obj.emergencymobileno=request.params['emermobil']
                request.dbsession.add(obj)

                print("inserted into houseowner")
                request.session.flash('Houseowner Added')
                url = request.route_url('listhouseowner')
                return HTTPFound(location=url)
            else:
                print("houseownerpg")
            return dict()
        raise Exception('You are a houseowner')
    except:
        url = request.route_url('logintype')
        return HTTPFound(location=url)


@view_config(route_name = 'list_block',renderer= '../templates/list_block.jinja2')  
def list_block(request):
    try:
        if request.method == 'GET' and request.session['role']=='admin':
            return dict()
        raise Exception('you are a houseowner')
    except:
        url = request.route_url('logintype')
        return HTTPFound(location=url)


@view_config(route_name='listhouseowner', renderer='../templates/listhouseowner.jinja2')
def listhouseowner(request):
    messages = request.session.pop_flash()
    if request.method == 'POST':
        if (request.params['sector'].lower() !='all sectors'):
            search = "%{}%".format(request.params['sector'].upper())
        else:
            search = "%{}%".format('')  
        result = request.dbsession.query(Houseowner).filter(Houseowner.username.like(search)).order_by(Houseowner.username)
        return dict(result=result,messages=messages,ct=result.count())
    try:
        if request.method == 'GET' and request.session['role']=='admin':
            result = request.dbsession.query(Houseowner).all()
            return dict(result=result,messages=messages)
        raise Exception('you are a houseowner')
    except:
        url = request.route_url('logintype')
        return HTTPFound(location=url)


@view_config(route_name='houseownerlogin', renderer='../templates/login.jinja2')
def houseownerlogin(request):
    if request.method=='POST':
        username=request.params['username']
        password=request.params['password']
        query = request.dbsession.query(Houseowner)
        one = query.filter(and_(Houseowner.username == username,Houseowner.password==password)).first()
        if one:
            session = request.session
            session['user']  = username
            session['role']  = "houseowner"
            request.session['houseownername']=one.houseownername
            url = request.route_url('listtenantpg')
            return HTTPFound(location=url)
        else:
            return dict(msg="Wrong username or password.Try again or click forgot password to reset it.")


    return dict()


@view_config(route_name='listtenantpg',renderer='templates/list.jinja2')
def list(request):
    try:
        if request.session['role']=='houseowner':
                print()
                print()
                print()
                print(request.session)
                print()
                messages = request.session.pop_flash()
                name=request.session['houseownername']
                query = request.dbsession.query(Houseowner)
                one = query.filter(Houseowner.houseownername == name).first()

                query2 = request.dbsession.query(Tenant)
                result=query2.filter(Tenant.houseownerid ==one.houseownerid )
                for row in result:
                    print(row.tenantname)
                return dict(result=result,messages=messages,one=one)
        raise Exception('You are a admin')
    except:
        url = request.route_url('logintype')
        return HTTPFound(location=url)


@view_config(route_name='addtenantpg', renderer='../templates/kyc.jinja2')
def addtenantpg(request):
    if request.method=='POST':
        name=request.session['houseownername']
        print(name)
        query = request.dbsession.query(Houseowner)
        one = query.filter(Houseowner.houseownername == name).first()
        #result=Session.query(Houseowner).filter(Houseowner.houseownername==name)

        obj1=Tenant()
        obj1.houseownerid=one.houseownerid
        obj1.sector=request.params['sector']
        obj1.houseno=request.params['house_no']
        obj1.tenantname=request.params['tenantname']
        obj1.fathername=request.params['fathername']
        obj1.permanentaddress=request.params['address1']
        obj1.mobileno=request.params['ph_no1']
        obj1.landlineno=request.params['landline_no1']
        obj1.emailid=request.params['email1']
        obj1.occupation=request.params['occupation1']
        obj1.noofadults=request.params['adults']
        obj1.noofchildren=request.params['noofchildern']
        obj1.noofpersons=request.params['total_persons']
        obj1.nooftwowheelers=request.params['two_wheeler']
        obj1.nooffourwheelers=request.params['four_wheeler']
        obj1.totalnoveh=request.params['total_vehicles']
        obj1.emergencycontactname=request.params['emername']
        obj1.emergencymobileno=request.params['emermobil']

        tot=int(request.params['total_vehicles'])
        request.dbsession.add(obj1)
        query = request.dbsession.query(Tenant)
        one = query.filter(Tenant.tenantname == request.params['tenantname']).first()
        tenantid=one.tenantid

        vtype=request.POST.getall('vtype[]')
        vmake=request.POST.getall('vmake[]')
        vno=request.POST.getall('vno[]')
        vcolor=request.POST.getall('vcolor[]')
        print("vtype:",vtype)
        print("vmake",vmake)
        for i in range(tot):
            veh=Vehicle()
            if vtype[i]:
                veh.vehicletype=vtype[i]
            if vmake[i]:
                veh.vehiclemake=vmake[i]
            if vno[i]:
                veh.regno=vno[i]
            if vcolor[i]:
                veh.color=vcolor[i]

            veh.tenantid=tenantid
            request.dbsession.add(veh)




        request.session.flash('Tenant Added')

        url = request.route_url('listtenantpg')
        return HTTPFound(location=url)
    print("tenantpg")
    return dict()
@view_config(route_name='deletehouseowner')
def deletehouseowner(request):
    try:
        if request.session['role']=='admin': 
            houseownerid = int(request.matchdict.get('id'))
            query = request.dbsession.query(Houseowner)
            one = query.filter(Houseowner.houseownerid == houseownerid).first()
            request.dbsession.delete(one)
            request.session.flash('Houseowner Deleted')
            url = request.route_url('listhouseowner')
            return HTTPFound(location=url)
        raise Exception('You are a houseowner')
    except:
        url = request.route_url('logintype')
        return HTTPFound(location=url)


@view_config(route_name='deletetenantpg')
def deletetenantpg(request):
    try:
        if request.session['role']=='houseowner':
            tenantid = int(request.matchdict.get('id'))
            query = request.dbsession.query(Tenant)
            one = query.filter(Tenant.tenantid == tenantid).first()
            request.dbsession.delete(one)
            request.session.flash('Tenant Deleted')
            url = request.route_url('listtenantpg')
            return HTTPFound(location=url)
        raise Exception('You are a admin')
    except:
        url = request.route_url('logintype')
        return HTTPFound(location=url)
        

@view_config(route_name='edittenantpg', renderer='../templates/edit.jinja2')
def edittenantpg(request):
    try:
        if request.session['role']=='houseowner':
            tenantid = int(request.matchdict.get('id'))
            query = request.dbsession.query(Tenant)
            one = query.filter(Tenant.tenantid == tenantid).first()
            veh=request.dbsession.query(Vehicle).filter(Vehicle.tenantid == tenantid)
            # print(one.emergencycontactname)
            # print(one.permanentaddress)
            if request.method=='POST':
                print("in edittenantpg post")
                one.tenantname=request.params['tenantname']
                one.sector=request.params['sector']
                one.houseno=request.params['house_no']

                one.fathername=request.params['fathername']
                one.permanentaddress=request.params['address1']
                one.mobileno=request.params['ph_no1']
                one.landlineno=request.params['landline_no1']
                one.emailid=request.params['email1']
                one.occupation=request.params['occupation1']
                one.noofadults=request.params['adults']
                one.noofchildren=request.params['noofchildern']
                one.noofpersons=request.params['total_persons']
                one.nooftwowheelers=request.params['two_wheeler']
                one.nooffourwheelers=request.params['four_wheeler']
                one.totalnoveh=request.params['total_vehicles']
                one.emergencycontactname=request.params['emername']
                one.emergencymobileno=request.params['emermobil']
                vtype=request.POST.getall('vtype[]')
                vmake=request.POST.getall('vmake[]')
                vno=request.POST.getall('vno[]')
                vcolor=request.POST.getall('vcolor[]')
                i=0
                for v in veh:
                    # vehi=request.dbsession.query(Vehicle).filter(Vehicle.regno == vno[i]).first()
                    if v:
                        if vtype[i]:
                            v.vehicletype=vtype[i]
                        if vmake[i]:
                            v.vehiclemake=vmake[i]
                        if vno[i]:
                            v.regno=vno[i]
                        if vcolor[i]:
                            v.color=vcolor[i]
                        i=i+1


                    request.session.flash('Tenant Edited')
                url = request.route_url('listtenantpg')
                return HTTPFound(location=url)

            return dict(one=one,id=tenantid,veh=veh)
        raise Exception('You are a admin')
    except:
        url = request.route_url('logintype')
        return HTTPFound(location=url)


def isInteger(reqParm):
    if(type(reqParm)==type(1)):
        return int(reqParm)
    else:
        return 0


@view_config(route_name='editthouseowner', renderer='../templates/edithouseowner.jinja2')
def editthouseowner(request):
    try:
        if request.session['role']=='admin' or request.session['role']=='houseowner':
            houseownerid = int(request.matchdict.get('id'))
            query = request.dbsession.query(Houseowner)
            one = query.filter(Houseowner.houseownerid == houseownerid).first()
            query = request.dbsession.query(Tenant)
            two = query.filter(Tenant.houseowner == one).first()
            query = request.dbsession.query(Vehicle)
            three = query.filter(Vehicle.tenantid == two.tenantid)

            try:
                if request.method=='POST':
                    print("in editthouseowner post")
                    one.houseownername=request.params['houseownername']
                    one.password=request.params['password']
                    one.username =request.params['username']
                    one.fathername=request.params['fathername']
                    one.permanentaddress =request.params['address']
                    one.contactmobileno=request.params['ph_no']
                    one.landline_no=request.params['landline_no']
                    one.emailid=request.params['email']
                    one.emergencycontactname=request.params['emername']
                    one.emergencymobileno=request.params['emermobil']

                    two.sector=request.params['sector']
                    two.houseno=request.params['house_no']
                    two.tenantname=request.params['tenantname']
                    two.fathername=request.params['fathername1']
                    two.permanentaddress=request.params['address1']
                    two.mobileno=request.params['ph_no1']
                    two.landlineno=request.params['landline_no1']
                    two.emailid=request.params['email1']
                    two.occupation=request.params['occupation1']
                    try:
                        two.noofadults=request.params['adults']
                    except:
                        two.noofadults=0
                    try:
                        two.noofchildren= int(request.params['noofchildern'])
                    except:
                        two.noofchildren=0
                    try:
                        two.nooftwowheelers=int(request.params['two_wheeler'])
                    except:
                        two.nooftwowheelers=0
                    try:
                        two.nooffourwheelers=int(request.params['four_wheeler'])
                    except:
                        two.nooffourwheelers=0
                    two.noofpersons=int(two.noofadults) + int(two.noofchildren)
                    two.totalnoveh=int(two.nooftwowheelers) + int( two.nooffourwheelers)


                    vtype=request.POST.getall('vtype[]')
                    vmake=request.POST.getall('vmake[]')
                    vno=request.POST.getall('vno[]')
                    vcolor=request.POST.getall('vcolor[]')

                    # print(vno)
                    i=0
                    for v in three:
                        try:
                        # vehi=request.dbsession.query(Vehicle).filter(Vehicle.regno == vno[i]).first()
                            if(i>3):
                                break
                            if v:
                                if vtype[i]:
                                    v.vehicletype=vtype[i]
                                if vmake[i]:
                                    v.vehiclemake=vmake[i]
                                if vno[i]:
                                    v.regno=vno[i]
                                if vcolor[i]:
                                    v.color=vcolor[i]
                                i=i+1
                        except:
                            continue

                    # for i in range(5):
                    #     try:
                    #         three[i].vehicletype=vtype[i]
                    #         three[i].vehiclemake=vmake[i]
                    #         three[i].regno=vno[i]
                    #         three[i].color=vcolor[i]
                    #     except:
                    #         continue

                    request.session.flash('Houseowner Edited')
                    session=request.session
                    if 'houseownername' in session:
                        request.session['houseownername']=request.params['houseownername']
                        url = request.route_url('listtenantpg')
                        return HTTPFound(location=url)

                    url = request.route_url('listhouseowner')
                    return HTTPFound(location=url)
            except:
                return dict(one=one,two=two,three=three,id=houseownerid)

            return dict(one=one,two=two,three=three,id=houseownerid)
        raise Exception('You are a houseowner')
    except:
        url = request.route_url('logintype')
        return HTTPFound(location=url)


@view_config(route_name='viewtenantpg', renderer='../templates/view.jinja2')
def viewtenantpg(request):
    try:
        if request.session['role']=='houseowner':    
            tenantid = int(request.matchdict.get('id'))
            query = request.dbsession.query(Tenant)
            one = query.filter(Tenant.tenantid == tenantid).first()
            return dict(one=one)
        raise Exception('You are a admin')
    except:
        url = request.route_url('logintype')
        return HTTPFound(location=url)


@view_config(route_name='viewhouseowner', renderer='../templates/viewhouseowner.jinja2')
def viewhouseowner(request):
    try:
        if request.session['role']=='admin':
            houseownerid = int(request.matchdict.get('id'))
            query = request.dbsession.query(Houseowner)
            one = query.filter(Houseowner.houseownerid == houseownerid).first()
            query = request.dbsession.query(Tenant)
            two = query.filter(Tenant.houseownerid == houseownerid).all()
            return dict(one=one,two=two)
        raise Exception('You are a houseowner')
    except:
        url = request.route_url('logintype')
        return HTTPFound(location=url)
#ok


@view_config(route_name='adminaddtenantpg', renderer='../templates/tenant.jinja2')
def adminaddtenantpg(request):
    try:
        if request.session['role']=='admin' or request.session['role']=='houseowner':
            houseownerid = int(request.matchdict.get('id'))
            if request.method=='POST':

                obj1=Tenant()
                obj1.houseownerid=houseownerid
                obj1.sector=request.params['sector']
                obj1.houseno=request.params['house_no']
                obj1.tenantname=request.params['tenantname']
                obj1.fathername=request.params['fathername']
                obj1.permanentaddress=request.params['address1']
                obj1.mobileno=request.params['ph_no1']
                obj1.landlineno=request.params['landline_no1']
                obj1.emailid=request.params['email1']
                obj1.occupation=request.params['occupation1']
                obj1.noofadults=request.params['adults']
                obj1.noofchildren=request.params['noofchildern']
                obj1.noofpersons=request.params['total_persons']
                obj1.nooftwowheelers=request.params['two_wheeler']
                obj1.nooffourwheelers=request.params['four_wheeler']
                obj1.totalnoveh=request.params['total_vehicles']
                obj1.emergencycontactname=request.params['emername']
                obj1.emergencymobileno=request.params['emermobil']
                tot=int(request.params['total_vehicles'])
                request.dbsession.add(obj1)
                query = request.dbsession.query(Tenant)
                one = query.filter(Tenant.tenantname == request.params['tenantname']).first()
                tenantid=one.tenantid

                vtype=request.POST.getall('vtype[]')
                vmake=request.POST.getall('vmake[]')
                vno=request.POST.getall('vno[]')
                vcolor=request.POST.getall('vcolor[]')
                for i in range(tot):
                    veh=Vehicle()
                    if vtype[i]:
                        veh.vehicletype=vtype[i]
                    if vmake[i]:
                        veh.vehiclemake=vmake[i]
                    if vno[i]:
                        veh.regno=vno[i]
                    if vcolor[i]:
                        veh.color=vcolor[i]
                    veh.tenantid=tenantid
                    request.dbsession.add(veh)

                url = request.route_url('listhouseowner')
                return HTTPFound(location=url)
            return dict(id=houseownerid)
        raise Exception('You must login')
    except:
        url = request.route_url('logintype')
        return HTTPFound(location=url)


@view_config(route_name='admindeletetenant')
def admindeletetenant(request):
    try:
        if request.session['user']=='admin':
            tenantid = int(request.matchdict.get('id'))
            query = request.dbsession.query(Tenant)
            one = query.filter(Tenant.tenantid == tenantid).first()
            request.dbsession.delete(one)
            url = request.route_url('listhouseowner')
            return HTTPFound(location=url)
        raise Exception('You are a houseowner')
    except:
        url = request.route_url('logintype')
        return HTTPFound(location=url)


@view_config(route_name='logintype', renderer='../templates/loginas.jinja2')
def logintype(request):
    
    request.session.invalidate()
    return dict()
@view_config(route_name='adminlogin', renderer='../templates/adminlogin.jinja2')
def adminlogin(request):
    if request.method=='POST':
        adminname=request.params['username']
        password=request.params['password']
        query = request.dbsession.query(User_Admin)
        one = query.filter(and_(User_Admin.username == adminname,User_Admin.password==password)).first()
        if one:
            session = request.session
            session['user']  = adminname
            session['role']  = "admin"
            url = request.route_url('list_block')
            return HTTPFound(location=url)
        else:
            return dict(msg="Invalid Login")


    return dict()

@view_config(route_name='searchtype', renderer='../templates/searchresult.jinja2')
def searchtype(request):
    try:
        if request.session['role']=='admin':
            if request.method=='POST':
                type=int(request.params['select'])
                if type==1:

                    houseownername=request.params['name']

                    #print(houseownername2)
                    p='%'
                    search_by_name=request.dbsession.query(Houseowner,Tenant).filter(and_(Houseowner.houseownerid == Tenant.houseownerid,Houseowner.houseownername.like( p+houseownername+p)))
                    #search_by_name=request.dbsession.query.filter(Houseowner.houseownername.like(houseownername2))

                    if search_by_name:
                        print("nope")
                    print("inside search")
                    for h,t in search_by_name:
                        if h.houseownername:
                            return dict(result=search_by_name,houseownername=h.houseownername,type=type)
                    row=request.dbsession.query(Houseowner).filter(Houseowner.houseownername == houseownername).first()
                    if row:
                        print("helo")
                        print(row.fathername)
                        return dict(row=row,houseownername=row.houseownername,type=type)
                    print("name not found check new")
                    return dict(msg="Data does not exist")
                elif type==2:
                    tenantname=request.params['name']
                    p='%'
                    row=request.dbsession.query(Tenant).filter(Tenant.tenantname.like( p+tenantname+p)).first()
                    if row:
                        tenantid=row.tenantid
                        #tenantname=row.tenantname
                        Vehicles=request.dbsession.query(Vehicle).filter(Vehicle.tenantid== tenantid)
                        return dict(result=row,type=type,Vehicles=Vehicles)
                    return dict(msg="Data does not exist")
                elif type==3:
                    p='%'
                    regno=request.params['name']
                    search_by_vehicle_reg_no=request.dbsession.query(Tenant,Vehicle).filter(and_(Tenant.tenantid==Vehicle.tenantid,Vehicle.regno.like(p+regno+p)))
                    for t,v in search_by_vehicle_reg_no:
                        if v.regno:
                            return dict(result=search_by_vehicle_reg_no,type=type,regno=regno)
                    print("name not found")
                    return dict(msg="Data does not exist")
                elif type==4:
                    p='%'
                    houseno=request.params['name']
                    search_by_houseno=request.dbsession.query(Houseowner,Tenant).filter(and_(Houseowner.houseownerid == Tenant.houseownerid,Tenant.houseno.like(p+houseno+p)))
                    for h,t in search_by_houseno:
                        if t.houseno:
                            return dict(result=search_by_houseno,type=type,houseno=houseno)
                    print("name not found")
                    return dict(msg="Data does not exist")
                elif type==5:
                    check=request.dbsession.query(Houseowner,Tenant).filter(Houseowner.houseownerid == Tenant.houseownerid).order_by(Houseowner.houseownerid)
                    for h,t in check:
                        if h.houseownerid:
                            return dict(result=check,type=type)
                    print("name not found")
                    return dict(msg="Data does not exist")
        raise Exception('You are a houseowner')
    except:
        url = request.route_url('logintype')
        return HTTPFound(location=url)


    return dict()
db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_agrini_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""