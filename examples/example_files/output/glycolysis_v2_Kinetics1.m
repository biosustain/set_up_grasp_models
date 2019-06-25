function [f,grad] = glycolysis_v2_Kinetics1(x,model,fixedExch,Sred,kinInactRxns,subunits,flag)
% Pre-allocation of memory
h = 1e-8;
% Defining metabolite and enzyme species
if flag==1
x = x(:);
v = zeros(22,36);
E = zeros(22,36);
x = [x,x(:,ones(1,35)) + diag(h*1i*ones(35,1))];
else
v = zeros(22,size(x,2));
E = zeros(22,size(x,2));
end
% Defining metabolite and enzyme species
m_m_g6p_c = x(1,:);
m_m_6pgl_c = x(2,:);
m_m_6pgc_c = x(3,:);
m_m_2ddg6p_c = x(4,:);
m_m_g3p_c = x(5,:);
m_m_pyr_c = x(6,:);
m_m_f6p_c = x(7,:);
m_m_fdp_c = x(8,:);
m_m_dhap_c = x(9,:);
m_m_13dpg_c = x(10,:);
m_m_3pg_c = x(11,:);
m_m_2pg_c = x(12,:);
m_m_pep_c = x(13,:);
E(1,:) = x(14,:);
E(2,:) = x(15,:);
E(3,:) = x(16,:);
E(4,:) = x(17,:);
E(5,:) = x(18,:);
E(6,:) = x(19,:);
E(7,:) = x(20,:);
E(8,:) = x(21,:);
E(9,:) = x(22,:);
E(10,:) = x(23,:);
E(11,:) = x(24,:);
E(12,:) = x(25,:);
E(13,:) = x(26,:);
E(14,:) = x(27,:);
E(15,:) = x(28,:);
E(16,:) = x(29,:);
E(17,:) = x(30,:);
E(18,:) = x(31,:);
E(19,:) = x(32,:);
E(20,:) = x(33,:);
E(21,:) = x(34,:);
E(22,:) = x(35,:);
% Reaction rates
v(1,:) = r_R_G6PDH21([ones(1,size(x,2));m_m_g6p_c;m_m_6pgl_c;ones(1,size(x,2))],model.rxnParams(1).kineticParams);
v(2,:) = r_R_G6PDH2_NAD1([ones(1,size(x,2));m_m_g6p_c;m_m_6pgl_c;ones(1,size(x,2))],model.rxnParams(2).kineticParams);
v(3,:) = r_R_G6PDH2_NADP1([ones(1,size(x,2));m_m_g6p_c;m_m_6pgl_c;ones(1,size(x,2))],model.rxnParams(3).kineticParams);
v(4,:) = r_R_PGL1([m_m_6pgl_c;m_m_6pgc_c],model.rxnParams(4).kineticParams);
v(5,:) = r_R_EDD1([m_m_6pgc_c;m_m_2ddg6p_c],model.rxnParams(5).kineticParams);
v(6,:) = r_R_EDA1([m_m_2ddg6p_c;m_m_g3p_c;m_m_pyr_c],model.rxnParams(6).kineticParams);
v(7,:) = r_R_PGI1([m_m_g6p_c;m_m_f6p_c],model.rxnParams(7).kineticParams);
v(8,:) = r_R_FBP1([m_m_fdp_c;m_m_f6p_c;ones(1,size(x,2))],model.rxnParams(8).kineticParams);
v(9,:) = r_R_FBA1([m_m_dhap_c;m_m_g3p_c;m_m_fdp_c],model.rxnParams(9).kineticParams);
v(10,:) = r_R_TPI1([m_m_g3p_c;m_m_dhap_c],model.rxnParams(10).kineticParams);
v(11,:) = r_R_GAPD1([ones(1,size(x,2));m_m_g3p_c;ones(1,size(x,2));m_m_13dpg_c;ones(1,size(x,2))],model.rxnParams(11).kineticParams);
v(12,:) = r_R_PGK1([ones(1,size(x,2));m_m_13dpg_c;m_m_3pg_c;ones(1,size(x,2))],model.rxnParams(12).kineticParams);
v(13,:) = r_R_PGM1([m_m_3pg_c;m_m_2pg_c],model.rxnParams(13).kineticParams);
v(14,:) = r_R_ENO1([m_m_2pg_c;m_m_pep_c],model.rxnParams(14).kineticParams);
v(15,:) = r_R_PYK1([ones(1,size(x,2));m_m_pep_c;ones(1,size(x,2));m_m_pyr_c],model.rxnParams(15).kineticParams);
v(16,:) = r_R_EX_pyr1(m_m_pyr_c,ones(1,size(x,2)),model.rxnParams(16).kineticParams);
v(17,:) = r_R_EX_pep1(m_m_pep_c,ones(1,size(x,2)),model.rxnParams(17).kineticParams);
v(18,:) = r_R_EX_g6p1(m_m_g6p_c,ones(1,size(x,2)),model.rxnParams(18).kineticParams);
v(19,:) = r_R_EX_6pgc1(ones(1,size(x,2)),m_m_6pgc_c,model.rxnParams(19).kineticParams);
v(20,:) = r_R_EX_g3p1(m_m_g3p_c,ones(1,size(x,2)),model.rxnParams(20).kineticParams);
v(21,:) = r_R_EX_f6p1(m_m_f6p_c,ones(1,size(x,2)),model.rxnParams(21).kineticParams);
v(22,:) = r_R_EX_3pg1(m_m_3pg_c,ones(1,size(x,2)),model.rxnParams(22).kineticParams);
if flag==1
% Final rates
y = sum((Sred*(E.*v)).^2);
f = real(y(1));
if (nargout>1) % gradient is required
grad = imag(y(2:end))/h;
end
else
f = E.*v;
grad = [];
end
