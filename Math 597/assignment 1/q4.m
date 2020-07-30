m = 100;
x_data = (rand(m,1)*2)-1;
x_k = rand(1); %initial estimate
L=1;
h_k = 1/(2*L);
iterMax = 100;
f_k = zeros(iterMax,1);

%known best values
x_star = sum(x_data)/m;
f_star = func(x_star,m,x_data);

%perform gradient descent until the difference between f_k and f* comes close to MATLABs float precision
iter = 1;
while iter < iterMax
    df = derivative(x_k,m,x_data);
    x_k = x_k - h_k*df;
    f_k(iter) = func(x_k,m,x_data);
    %if (f_k(iter) - f_star) <= 1e-35
    %  break;
    %end
    x_k
    iter = iter + 1;
end

cla reset;
%Plot graph
x = 1:iter;
y = f_k(1:iter) - f_star;
%y = log(f_k(1:iter) - f_star);  
%plot(x,y,'-o','MarkerIndices',1:1:length(y))
scatter(x,y,'filled')
title('f(x_k) - f^* (Gradient Descent)')
xlabel('k') 
%ylabel('log(f(x_k)-f^*)');
set(gca, 'YScale', 'log')

%function f
function f = func(x,m,x_data)
    f = (sum((x_data-x).^2))/(2*m);
end

%derivative of f
function df = derivative(x,m,x_data)
    df = x - (sum(x_data)/m);
end