n = [1,2,3,4,5,6,7,8,9,10];
times = [0.0131;0.0542;0.1652; 0.5614;1.6412; 2.9546; 4.9099; 8.3626; 10.9059; 15.4361];

A = ones(10,4);
A(:,2) = [1;2;3;4;5;6;7;8;9;10];
A(:,3) = [1;4;9;16;25;36;49;64;81;100];
A(:,4) = [1;8;27;64;125;216;343;512;729;1000];

A;

[Q,R] = qr(A,0);
alpha = inv(R)*(Q'*times);
alpha

scatter(n,times);
hold on
x = linspace(0,10);
y = alpha(1) + alpha(2)*x + alpha(3)*x.^2 + alpha(4)*x.^3;
plot(x,y)
axis([0.5 10.5 -0.5 25])
legend({'Timing Data',' QR decomposition Least Squares Solution'},'Location','northwest')
title('Householder QR Decomposition on Matrix A of size (100*n,50*n)')
xlabel('n') 
ylabel('Computation Time (Seconds)')