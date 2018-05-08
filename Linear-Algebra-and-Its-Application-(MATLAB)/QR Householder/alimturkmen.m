load('/home/alim/Dropbox/CMPE482_Fall2017/Homework2/hw2_data.mat');


% The problem is modelled as A*x= b
% A is the database stands for past eqrthquakes.
% v1 is the number of earthquakes happened a year before
% v2 is the number of earthquakes happened two years before
% v3 is the number of earthquakes happened three years before
v1 = X(3:99, 2);
v2 = X(2:98, 2);
v3 = X(1:97, 2);
A = [ones(97,1) v1 v2 v3];
% b is the actual numbers of earthquakes
b = X(4:100,2);
% Aqr contains both R matrix and v columns
Aqr = qr_householder(A);
[m, n] = size(A);
% Gets R from the whole matrix
R = triu(Aqr);
% Gets rid of the zero values.
R = R(1:m, 1:n);
% Since x = R\(Q'*b) and we don't have Q matrix, 
QX = b;
% Takes vi vector and constructs Qi, then multiplies it with b.
for i=1:n
    % Temp = Qi
    Temp = zeros(m, m);
    Temp(1:i-1, 1:i-1) = eye(i-1);
    % Qi = I-2vivi*
    Temp(i:m, i:m)= eye(m-i+1) - 2*Aqr(i+1:m+1,i)*Aqr(i+1:m+1,i)';
    % QX = Qn....Q2Q1x
    QX = Temp*QX;
end

%x stores the coefficients ß0, ß1, ß2 and ß3 .
x = R\QX;




