%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 3.1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% To delete knowledgebase, the predicates that will be deleted 
% should be made dynamic. To get the number of each predicates, 
% StudentList(see part 3.2), SlotList and RoomList are created and length
% of these lists are written. Then by using 'retractall/1' all of the 
% predicates are deleted from the knowledgebase
:- dynamic student/2, available_slots/1, room_capacity/2.
clear_knowledge_base :- all_students(StudentList), length(StudentList, NumberofStudents),
			write('student/2: '), writeln(NumberofStudents),
			findall(Slot, available_slots(Slot), SlotList), length(SlotList, NumberofSlots), 
			write('available_slots/1 : '), writeln(NumberofSlots),
			findall(Room, room_capacity(Room, _), RoomList), length(RoomList, NumberofRooms),
			write('room_capacity/2: '), writeln(NumberofRooms),
			retractall(student(_,_)), retractall(available_slots(_)), retractall(room_capacity(_, _)).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 3.2 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Finds all the students with their ids and store them in a list 
% called StudentList.
all_students(StudentList) :- findall(Id, student(Id,_), StudentList).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 3.3 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Looks all students' courselists and finds the members of these 
% courselists and store them in CourseList2. Then to avoid duplication,
% 'list_to_set/2' eliminates the dublicates.
all_courses(CourseList) :- findall(Course, (student(_,Courses), member(Course,Courses)), CourseList2), 
			list_to_set(CourseList2, CourseList).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 3.4 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Looks all the students' courselists and adds the courselists in a
% list named StudentsTakingCourseId. 'length/2' finds the length of 
% StudentsTakingCourseId.
student_count(CourseId, StudentCount) :- findall(Courses, (student(_,Courses), member(CourseId,Courses)), StudentsTakingCourseId), 
					length(StudentsTakingCourseId, StudentCount). 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 3.5 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Finds all the courselists(Courses) which contain both CoureId1 and
% CourseId2 and stores these courselists in STakingCourseId1and2.
% Finally finds the length(StudentCount) of STakingCourseId1and2.
common_students(CourseId1, CourseId2, StudentCount) :-  findall(Courses, (student(_,Courses), member(CourseId2,Courses), member(CourseId1,Courses)), STakingCourseId1and2), 
							length(STakingCourseId1and2,StudentCount).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 3.6 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Looks all the list of slots (available_slots/1), and takes all the
% members of these lists and store them in SlotList
slot_list(SlotList) :- findall(Slot, (available_slots(SlotList2), 
			member(Slot, SlotList2)), SlotList).

% The aim of this predicate is basicly, by finding all the room-slot 
% combinations without repetition, increasing the readibility and
% writability of 'final_plan/1'. 'room_slot2/2' is the assistant rule of
% 'room_slot/1'. 'room_slot', takes the first element of the slotlist and 
% a room from 'room_capacity/2' then makes a pair of a room and a slot
% and store these pairs in RoomAndSlot2 list. After then sends
% the rest of the slotlist and a new list named RoomAndSlot3 to
% 'room_slot2/2'. Then appends RoomAndSlot2 and RoomAndSlot3 in the list
% that we are looking for, RoomAndSlot. 
% RoomAndSlot3 is the list that contains the combination
% of rooms with the rest of the elements of the slotlist. 'room_slot2/2'
% does the same job with 'room_slot/1' until it reaches the last element 
% of the slotlist. Then appending all of these pair lists we get
% RoomAndSlot which contains all possible room-slot pairs.
room_slot2(RoomAndSlot, [Slot]) :- findall([Room, Slot], (room_capacity(Room,_)), RoomAndSlot).
room_slot2(RoomAndSlot, [Slot|Tail]) :- findall([Room, Slot], (room_capacity(Room,_)), RoomAndSlot2), 
					room_slot2(RoomAndSlot3, Tail), 
					append(RoomAndSlot2, RoomAndSlot3, RoomAndSlot).
room_slot(RoomAndSlot) :- slot_list([Slot|Tail]), findall([Room, Slot], (room_capacity(Room,_)), RoomAndSlot2), 
					room_slot2(RoomAndSlot3, Tail),
					append(RoomAndSlot2, RoomAndSlot3, RoomAndSlot).

% Here 'final_plan2/2' is slight different version of 'final_plan/1'. 
% Addition to 'final_plan/1', 'final_plan2/2' takes a list of courses.
% The idea behind this rule is like this: 
%  It takes the first elements of FinalPlan and the courselist
%  and sends the rest of the lists to 'final_plan2/2'. It does the same job
%  until it reaches the last elements of FinalPlan and the courselist. 
%  For the last element of FinalPlan, it takes the last element of the
%  courselist as a course and finds a room-slot pair for this course and
%  checks whether it cause any errors by 'errors_for_plan/2'( see part 3.7).
%  Then it comes the second last element of FinalPlan. For the second 
%  last element of FinalPlan, it takes the second last element of the
%  courselist as a course and finds a room-slot pair for this course. 
%  There shouldn't be any trio with this chosen room-slot  pair in the 
%  tail of FinalPlan. Hence, it finds a room-slot pair that  is not used 
%  before by using member predicate. Finally checks whether it causes any
%  errors. It goes on like this till the first element. Changing the
%  room-slot pairs it finds all the possible FinalPlans. 
final_plan2([[Course,Room,Slot]], [Course]) :- room_slot(RSList), 
						member([Room,Slot], RSList),
						errors_for_plan([[Course,Room,Slot]], 0).
final_plan2([[Course,Room,Slot]|Tail], [Course|Rest]) :- final_plan2(Tail, Rest),
							 room_slot(RSList),
							 member([Room,Slot], RSList),  \+ member([_,Room,Slot], Tail), 
							 errors_for_plan([[Course,Room,Slot]|Tail],0).
final_plan([[Course,Room,Slot]|Tail]) :- all_courses([Course|Rest]), 
					 final_plan2(Tail, Rest), 
					 room_slot(RSList), member([Room,Slot], RSList), \+ member([_,Room,Slot], Tail), 
					 errors_for_plan([[Course,Room,Slot]|Tail],0).
		
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 3.7 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% The aim of this predicate counting the students that have more than
% one exam in the same slot. Predicates takes the suggested finalplan's
% first element and sends the rest again to the same predicate. Does 
% the same job until it reaches the base predicate. 
% Basicly predicate finds all the courses which are at the same time 
% with the given course. Then gather them in CommonCourses.
% (see common_students_error/3) 
% It keeps adding the errors from tail to head. 
slot_errors_for_plan([], 0).
slot_errors_for_plan([[CourseId, _, Slot]|T], ErrorCount) :- slot_errors_for_plan(T, ErrorCount2),
 
							((findall(Course, member([Course, _, Slot], T), CommonCourses),
							 common_students_error(CommonCourses, CourseId, N), ErrorCount is ErrorCount2+N); 								 ErrorCount is ErrorCount2),!.

% common_students_error/2 takes a courseid and list of courses. Starting from head
% of the list to tail it looks whether there are students taking courses
% at the same time. If so adds it to N, if not goes on with next element.
% It checks the commonality of the courseid with the each course in the list.
common_students_error([], _, 0).
common_students_error([Head|Tail], CourseId, N1) :- common_students_error(Tail, CourseId, N2), 
						    common_students(Head, CourseId, N), N1 is N2+N.

% Again for each course, it calculates the number of students taking 
% that course and compares it with the room capacity. If there is no error
% for that course the number of errors is equal to tail's number of errors.
capacity_errors_for_plan([], 0).
capacity_errors_for_plan([[Course, Room, _]|T], ErrorCount) :- capacity_errors_for_plan(T, ErrorCount2), 
							       student_count(Course, Number), 
							       room_capacity(Room, Capacity), 
				((Number > Capacity, ErrorCount is ErrorCount2 + Number -  Capacity); ErrorCount is ErrorCount2),!.

% Briefly adds the number of slot errors and capacity errors.
errors_for_plan(L, N) :- slot_errors_for_plan(L, N1), capacity_errors_for_plan(L,N2), N is N1+N2,!.



