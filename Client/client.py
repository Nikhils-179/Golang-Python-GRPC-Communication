from python_pb_files import emp_pb2 as emp_pb
from python_pb_files import emp_pb2_grpc as emp_grpc
from google.protobuf import empty_pb2
import logging
import grpc
logging.basicConfig(format='%(asctime)s:%(name)s : %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

socket = 'localhost:50051'
channel = grpc.insecure_channel(socket)
client = emp_grpc.EmployeeManagementStub(channel)
log.info(f"Connected to the Server : {socket}")


def call_get_employee(emp_id : str):
    log.info(f"Calling GetEmployee with the employee id {emp_id}")
    try:
        res = client.getEmployee(emp_pb.EmployeeID(id=emp_id))
        log.info("Response")
        log.info(res)
    except grpc.RpcError as e:
        log.error(f"Errored while getting the employee of ID {emp_id}")
        log.error(e)


def call_create_employee(emp_id: str, first_name: str, last_name: str, role: str, home_addrs: str, mob_numbr: str, mailid : str):
    log.info(f"Creating employee with the employee id {emp_id}")

    req_pb = emp_pb.Employee(
        id=emp_id,
        first_name=first_name,
        last_name=last_name,
        role=role,
        contact=emp_pb.Contact(home_addr=home_addrs, mob_num=mob_numbr, mail_id=mailid)
        )
    try:
        res = client.setEmployee(req_pb)
        log.info(f"Successfully created the Employee with the ID {res.id}")
    except grpc.RpcError as e:
        log.error(f"Errored while creating the employye of ID {emp_id}")
        log.error(e)

def call_list_employee():
    log.info("Calling ListEmployee")
    res = client.listEmployees(empty_pb2.Empty())
    log.info("ListEmployee Results")
    for r in res:
        log.info(r)


def call_update_employee(emp_id: str, first_name: str, last_name: str, role: str, home_addrs: str, mob_numbr: str, mailid : str):
    log.info(f"Calling updateEmployee with the employee id {emp_id}")
    req_pb = emp_pb.Employee(
        id=emp_id,
        first_name=first_name,
        last_name=last_name,
        role=role,
        contact=emp_pb.Contact(home_addr=home_addrs, mob_num=mob_numbr, mail_id=mailid)
        )
    try:
        client.updateEmployee(req_pb)
        log.info("Successfully updated")
    except grpc.RpcError as e:
        log.error(f"Errored while updating the employee of ID {emp_id}")
        log.error(e)

def call_delete_employee(emp_id: str):
    log.info(f"Calling deleteEmployee with the employee id {emp_id}")
    try:
        client.deleteEmployee(emp_pb.EmployeeID(id=emp_id))
        log.info(f"Successfully deleted the employee of id {emp_id}")
    except grpc.RpcError as e:
        log.error(f"Errored while deleting the employee of ID {emp_id}")
        log.error(e)
        
# should return error
call_get_employee("1")

# success create
call_create_employee(emp_id="1",first_name="Logesh",last_name="Vel",role="ASE",home_addrs="Some addr",mob_numbr="123456",mailid="some@domain.com")

# success get
call_get_employee("1")

# success create
call_create_employee(emp_id="2",first_name="log",last_name="esh",role="SSE",home_addrs="address",mob_numbr="98765",mailid="sse@domain.com")

# success list
call_list_employee()

# should error. the emp id is already present
call_create_employee(emp_id="2",first_name="log",last_name="esh",role="SSE",home_addrs="address",mob_numbr="98765",mailid="sse@domain.com")

# success update
call_update_employee(emp_id="2",first_name="log",last_name="esh",role="updated role Engineer",home_addrs="address",mob_numbr="98765",mailid="sse@domain.com")

# success list
call_list_employee()

# success delete
call_delete_employee(emp_id="2")

# should error in update. the emp id is deleted so can't update
call_update_employee(emp_id="2",first_name="log",last_name="esh",role="updated role Engineer",home_addrs="address",mob_numbr="98765",mailid="sse@domain.com")

# should error delete. since the emp is already deleted
call_delete_employee(emp_id="2")