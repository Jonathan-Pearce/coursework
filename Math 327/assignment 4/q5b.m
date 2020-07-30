N=10
A = [1 3 1 3; 3 1 2 1; 1 2 1 2; 3 1 2 4]

%get maximum eigenvalue
lamda = max(eig(A));

%generate initial unit vector
q = rand(4,1);
q = q/norm(q);

differences = zeros(1,N)

%Power Method
for k = 1:N
	q = A*q;
	q = q/norm(q);
	lamda_k = q' * A * q;
	differences(k) = abs(lamda-lamda_k);
end

%plot
scatter([1:1:10],differences,'filled')
set(gca, 'YScale', 'log')
xlim([0.5 10.5]);
xlabel('number of iterations');
ylabel('absolute error');
title('Convergence of Power Method');