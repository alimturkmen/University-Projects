function Y = qr_householder(X)

    [m, n] = size(X);
    X = [X; zeros(1,n)];
    
    for k = 1:n
        x = X(k:m, k);
        e1 = [1; zeros(m-k,1)];
        vk = sign(x(1))*norm(x)*e1 + x;
        vk = vk/norm(vk);
        X(k:m, k:n) = X(k:m, k:n) - 2*vk*(vk'*X(k:m, k:n));
        X(k+1:m+1, k) = vk;
    end
    
    Y = X;
end

