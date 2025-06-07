CREATE TABLE Student (
    StudentID INT PRIMARY KEY,
    Name VARCHAR(100),
    CourseID INT,
    AttendanceRecordID INT
);

CREATE TABLE Course (
    CourseID INT PRIMARY KEY,
    CourseName VARCHAR(100),
    InstructorID INT
);

CREATE TABLE Attendance (
    AttendanceID INT PRIMARY KEY,
    StudentID INT FOREIGN KEY REFERENCES Student(StudentID),
    CourseID INT FOREIGN KEY REFERENCES Course(CourseID),
    Date DATETIME,
    Status VARCHAR(20)
);

CREATE TABLE LeaveRequest (
    LeaveID INT PRIMARY KEY,
    StudentID INT FOREIGN KEY REFERENCES Student(StudentID),
    LeaveDate DATETIME,
    LeaveReason VARCHAR(500),
    Status VARCHAR(20)
);
