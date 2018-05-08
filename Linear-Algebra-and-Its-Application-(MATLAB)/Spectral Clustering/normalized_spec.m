function [cluster, A, D, L, X, Y] = normalized_spec(data, K, sigma)
%  Constructs cluster vector of given data.

N = size(data, 1);
%% Step1
A = zeros(N, N); %Affinity matrix
for i=1:N
    for j=1:N
    	difference = data(i,:)-data(j,:);
    	distance_ij = sqrt(sum(difference .* difference));
        A(i, j) = exp(-distance_ij/(2*sigma^2));
        if(i == j)
            A(i, j) = 0;
        end
    end
end
%% Step2
D = zeros(N, N); %Diagonal matrix

for i=1:N
    D(i, i) = sum(A(i, :));
end

L = zeros(N, N); % Normalized Laplacian matrix (L = D^(-1/2) * A * D^(-1/2) )

for i=1:N
    for j=1:N
        L(i,j) = A(i,j) / (sqrt(D(i,i)) * sqrt(D(j,j)));  
    end
end

%% Step3
[eigenvectors, eigenvalues] = eig(L);

X = zeros(N, K); %K largest eigenvectors of L
size_eigenvectors = size(eigenvectors(1,:));
size_eigen = size_eigenvectors(1,2);
X(:, :) = eigenvectors(:, size_eigen-K+1:size_eigen);

%% Step4
Y = normc(X); %Renormalized X

%% Step 5-6
cluster = kmeans(Y, K);

title_ = 'Normalized spectral clustering for K=';
title_ = [title_ num2str(K, '%2d')];
for i=1:N
    switch cluster(i, 1)
        case 1
            plot(data(i,1), data(i,2), 'b.')
            hold on
        case 2
            plot(data(i,1), data(i,2), 'g.')
            hold on
        case 3
            plot(data(i,1), data(i,2), 'r.')
            hold on
        case 4
            plot(data(i,1), data(i,2), 'c.')
            hold on
        case 5
            plot(data(i,1), data(i,2), 'm.')
            hold on
        case 6
            plot(data(i,1), data(i,2), 'y.')
            hold on
        case 7
            plot(data(i,1), data(i,2), 'k.')
            hold on
    end
    title(title_);
end

end