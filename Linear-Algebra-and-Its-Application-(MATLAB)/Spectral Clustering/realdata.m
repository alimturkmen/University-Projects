load('realdata.mat');
% Since this time we want to divide the features into clusters I added the 
% odd number X's rows up and assigned the sum to the first column of Y.
% I did the same thing for even number X's rows and assigned the sum to the second
% column of Y. Where Y is the matrix features by samples. However none of
% the clustering functions worked. normalized_spec gives error and the
% unnormalized_spec and kmeans functions do not give meaningful results.
% The two columns of Y became so similar to each other that the result
% looks linear instead of clustered. I hope I didn't misunderstand
% everything.
m = size(X, 1);
n = size(X, 2);
Y = zeros(2, n);
for i=1:m
    if mod(i,2)==1
        Y(1,:) = Y(1,:) + X(i, :);
    else
        Y(2,:) = Y(2,:) + X(i, :);
    end
end

Y = Y';
Y = Y./m;

data = Y;
K = 7;
cluster = kmeans(Y, K);

%normalized_spec(Y, K, 1) This function doesn't work
%unnormalized_spec(Y, K, 1);

    %kmeans clustering%%
%title_ = 'K-Means clustering for K=';
%title_ = [title_ num2str(K, '%2d')];
%for i=1:n
%    switch cluster(i, 1)
%        case 1
%            plot(data(i,1), data(i,2), 'b.')
%            hold on
%        case 2
%            plot(data(i,1), data(i,2), 'g.')
%            hold on
%        case 3
%            plot(data(i,1), data(i,2), 'r.')
%            hold on
%        case 4
%            plot(data(i,1), data(i,2), 'c.')
%            hold on
%        case 5
%            plot(data(i,1), data(i,2), 'm.')
%            hold on
%        case 6
%            plot(data(i,1), data(i,2), 'y.')
%            hold on
%        case 7
%            plot(data(i,1), data(i,2), 'k.')
%            hold on
%    end
%    title(title_);
%end 

