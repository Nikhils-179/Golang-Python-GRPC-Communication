package main

import (
	"context"
	"fmt"
	"log"
	pb "microservicegopython/src/proto/emp"
	"net"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"

	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/emptypb"
)

const socket string = "localhost:50051"

var employeeList []*pb.Employee

type Server struct {
	pb.EmployeeManagementServer
}

func main() {
	lis, err := net.Listen("tcp", socket)
	if err != nil {
		log.Fatalln("Error occured while listening to :", socket, err)
	}
	log.Println("Server started at port 50051")

	s := grpc.NewServer()
	pb.RegisterEmployeeManagementServer(s, &Server{})
	err = s.Serve(lis)
	if err != nil {
		log.Fatalln("Error Occured while Serving:", socket, err)
	}

}

func (s *Server) GetEmployee(ctx context.Context, empID *pb.EmployeeID) (*pb.Employee, error) {
	log.Println("Hitted GetEmployee with the employee ID", empID.Id)

	for _, e := range employeeList {
		if e.Id == empID.Id {
			return e, nil
		}
	}
	return nil, status.Errorf(
		codes.NotFound,
		"Given Employee is not found",
	)
}

func (s *Server) SetEmployee(ctx context.Context, emp *pb.Employee) (*pb.EmployeeID, error) {
	log.Println("Hitted SetEmployee with the emp ID", emp.Id)
	log.Println("Checking whether the given emp id is already there")
	for _, e := range employeeList {
		if e.Id == emp.Id {
			log.Println("The Given employee ID is already present.So skipping the create process")
			return nil, status.Errorf(
				codes.AlreadyExists,
				"Given Employee ID already exists. use UpdateEmployee to update",
			)
		}
	}

	employeeList = append(employeeList, emp)
	empID := pb.EmployeeID{Id: string(emp.Id)}
	log.Println("Given employee ID doesnot exist.Succesfully created")
	return &empID, nil
}

func (s *Server) ListEmployees(emt *emptypb.Empty, stream pb.EmployeeManagement_ListEmployeesServer) error {
	log.Println("Hitted List Employee")
	for _, e := range employeeList {
		stream.Send(e)
	}
	return nil
}

func (s *Server) UpdateEmployee(ctx context.Context, emp *pb.Employee) (*emptypb.Empty, error) {
	log.Println("Hitted UpdateEmployee to update the Employee Id", emp.Id)

	for i, e := range employeeList {
		if e.Id == emp.Id {
			employeeList[i] = emp
			log.Println("Updated employee\n", emp)
			return &emptypb.Empty{}, nil
		}
	}

	log.Println("Employee not found to update")
	return nil, status.Errorf(
		codes.NotFound,
		"Given employeeId not found to update",
	)
}

func (s *Server) DeleteEmployee(ctx context.Context, empId *pb.EmployeeID) (*emptypb.Empty, error) {
	log.Println("Hitted DeleteEmployee to Delete the emp ", empId)

	for i, e := range employeeList {
		if e.Id == empId.Id {
			employeeList = append(employeeList[:i], employeeList[i+1:]...)
			log.Println("Deleted the Employee")
			fmt.Println(employeeList)
			return &emptypb.Empty{}, nil
		}
	}
	log.Println("Employee not found to delete")
	return nil, status.Errorf(
		codes.NotFound,
		"Given employee ID is not found to delete",
	)
}
