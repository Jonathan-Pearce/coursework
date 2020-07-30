n = [1,2,3,4,5,6,7,8,9,10];

scatter(n,Explicit)
hold on
scatter(n,Implicit)
axis([0.5 10.5 -0.5 25])
%legend()
legend({'Explicit','Implicit'},'Location','northwest')
title('Explicit and Implicit Householder Methods on Matrix A of size (100*n,50*n)')
xlabel('n') 
ylabel('Computation Time (Seconds)')