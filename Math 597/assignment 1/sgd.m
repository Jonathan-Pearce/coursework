m = 1000;
x_data = (rand(m,1)*2)-1;
x_k = rand(1); %initial estimate
L=1;
h_k = 1/(2*L);
iterMax = 400;
f_k = zeros(iterMax,1);
m_batch = 100;

%known best values
x_star = sum(x_data)/m;
f_star = func(x_star,m,x_data);

for i=1:400
    x_batch  = x_data(randsample(length(x_data),100),:);
    x_k = x_k - h_k*derivative(x_k,m_batch,x_batch);
    
    f_k(i) = func(x_k,m,x_data);
    
    if mod(i,100) == 0
        h_k = h_k/5;
    end
    
end

%Plot graph
x = 1:iterMax;
y = f_k - f_star;  
plot(x,y)
title('f(x_k) - f^* (SGD - typical run)')
xlabel('k') 
%ylabel('f(x_k)-f^*');
set(gca, 'YScale', 'log')

%function f
function f = func(x,m,x_data)
    f = (sum((x_data-x).^2))/(2*m);
end

%derivative of f
function df = derivative(x,m,x_data)
    df = x - (sum(x_data)/m);
end