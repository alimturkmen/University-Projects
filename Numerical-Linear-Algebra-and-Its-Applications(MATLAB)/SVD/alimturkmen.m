load('/home/alim/Desktop/desktop/Course Materials/CMPE482/CMPE482HW1');
for i=1:471
    for j=1:366
        if Y(i,j) ~= 0
            Y(i,j) = 1;
        end
        for k=1:14
            if X(i, j, k) ~= 0
                X(i, j, k) = log(X(i, j, k)) + 1;
            end
        end
    end
end

Z = zeros(471, 366);


for i=1:471
    for j=1:366
        for k=1:14
                Z(i, j) = Z(i, j) + X(i,j,k);
        end
    end
end


[U, S, V] = svd(Z);
figure;  plot(diag(S),'*'); ylabel('Singular Values'); xlabel('Index'); title('Singular Values')
K = [2 10 20 50 100 300];

Zk2 = U(:,1:2)*S(1:2,1:2)*V(:,1:2)';
Zk10 = U(:,1:10)*S(1:10,1:10)*V(:,1:10)';
Zk20 = U(:,1:20)*S(1:20,1:20)*V(:,1:20)';
Zk50 = U(:,1:50)*S(1:50,1:50)*V(:,1:50)';
Zk100 = U(:,1:100)*S(1:100,1:100)*V(:,1:100)';
Zk300 = U(:,1:300)*S(1:300,1:300)*V(:,1:300)';

Y = Y(:);
Zk2 = Zk2(:);
Zk10 = Zk10(:);
Zk20 = Zk20(:);
Zk50 = Zk50(:);
Zk100 = Zk100(:);
Zk300 = Zk300(:);

[a2 b2 c2 auc2] = perfcurve(Y, Zk2, 1);
[a10 b10 c10 auc10] = perfcurve(Y, Zk10, 1);
[a20 b20 c20 auc20] = perfcurve(Y, Zk20, 1);
[a50 b50 c50 auc50] = perfcurve(Y, Zk50, 1);
[a100 b100 c100 auc100] = perfcurve(Y, Zk100, 1);
[a300 b300 c300 auc300] = perfcurve(Y, Zk300, 1);

str = [{'K=2','AUC=', auc2}, {'K=10', 'AUC=', auc10}, {'K=20', 'AUC=', auc20}, {'K=50', 'AUC=', auc50}, {'K=100', 'AUC=', auc100}, {'K=300', 'AUC=', auc300}];

figure; 
subplot(3, 2, 1); plot(a2, b2); xlabel('FPR'); ylabel('TPR'); text(0.6, 0.5, str(1:3), 'FontSize', 8);
subplot(3, 2, 2); plot(a10, b10); xlabel('FPR'); ylabel('TPR'); text(0.6, 0.5, str(4:6), 'FontSize', 8);
subplot(3, 2, 3); plot(a20, b20); xlabel('FPR'); ylabel('TPR'); text(0.6, 0.5, str(7:9), 'FontSize', 8);
subplot(3, 2, 4); plot(a50, b50); xlabel('FPR'); ylabel('TPR'); text(0.6, 0.5, str(10:12), 'FontSize', 8);
subplot(3, 2, 5); plot(a100, b100); xlabel('FPR'); ylabel('TPR'); text(0.6, 0.5, str(13:15), 'FontSize', 8);
subplot(3, 2, 6); plot(a300, b300); xlabel('FPR'); ylabel('TPR'); text(0.6, 0.5, str(16:18), 'FontSize', 8);
suptitle('ROC plots for different K values');


