function y = model_v2_3_all_Kinetics1_ode(y,Eref,metsRefConc,model,fixedExch,Sred,kinInactRxns,subunits,flag)

v = zeros(49,size(Eref,2));
E = zeros(49,size(Eref,2));

m_m_glc__D_p = y(1,:);
m_m_atp_c = y(2,:);
m_m_glc__D_c = y(3,:);
m_m_adp_c = y(4,:);
m_m_g6p_c = y(5,:);
m_m_glcn_p = y(6,:);
m_m_glcn_c = y(7,:);
m_m_6pgc_c = y(8,:);
m_m_2dhglcn_p = y(9,:);
m_m_2dhglcn_c = y(10,:);
m_m_6p2dhglcn_c = y(11,:);
m_m_nadh_c = y(12,:);
m_m_nad_c = y(13,:);
m_m_nadph_c = y(14,:);
m_m_nadp_c = y(15,:);
m_m_6pgl_c = y(16,:);
m_m_ru5p__D_c = y(17,:);
m_m_r5p_c = y(18,:);
m_m_xu5p__D_c = y(19,:);
m_m_g3p_c = y(20,:);
m_m_s7p_c = y(21,:);
m_m_e4p_c = y(22,:);
m_m_f6p_c = y(23,:);
m_m_2ddg6p_c = y(24,:);
m_m_pyr_c = y(25,:);
m_m_fdp_c = y(26,:);
m_m_dhap_c = y(27,:);
m_m_13dpg_c = y(28,:);
m_m_3pg_c = y(29,:);
m_m_2pg_c = y(30,:);
m_m_pep_c = y(31,:);
m_m_h2o2_c = y(32,:);
m_m_gthrd_c = y(33,:);
m_m_gthox_c = y(34,:);
E(1,:) = Eref(1,:);
E(2,:) = Eref(2,:);
E(3,:) = Eref(3,:);
E(4,:) = Eref(4,:);
E(5,:) = Eref(5,:);
E(6,:) = Eref(6,:);
E(7,:) = Eref(7,:);
E(8,:) = Eref(8,:);
E(9,:) = Eref(9,:);
E(10,:) = Eref(10,:);
E(11,:) = Eref(11,:);
E(12,:) = Eref(12,:);
E(13,:) = Eref(13,:);
E(14,:) = Eref(14,:);
E(15,:) = Eref(15,:);
E(16,:) = Eref(16,:);
E(17,:) = Eref(17,:);
E(18,:) = Eref(18,:);
E(19,:) = Eref(19,:);
E(20,:) = Eref(20,:);
E(21,:) = Eref(21,:);
E(22,:) = Eref(22,:);
E(23,:) = Eref(23,:);
E(24,:) = Eref(24,:);
E(25,:) = Eref(25,:);
E(26,:) = Eref(26,:);
E(27,:) = Eref(27,:);
E(28,:) = Eref(28,:);
E(29,:) = Eref(29,:);
E(30,:) = Eref(30,:);
E(31,:) = Eref(31,:);
E(32,:) = Eref(32,:);
E(33,:) = Eref(33,:);
E(34,:) = Eref(34,:);
E(35,:) = Eref(35,:);
E(36,:) = Eref(36,:);
E(37,:) = Eref(37,:);
E(38,:) = Eref(38,:);
E(39,:) = Eref(39,:);
E(40,:) = Eref(40,:);
E(41,:) = Eref(41,:);
E(42,:) = Eref(42,:);
E(43,:) = Eref(43,:);
E(44,:) = Eref(44,:);
E(45,:) = Eref(45,:);
E(46,:) = Eref(46,:);
E(47,:) = Eref(47,:);
E(48,:) = Eref(48,:);
E(49,:) = Eref(49,:);
v(1,:) = r_R_GLCabcpp1([m_m_glc__D_p;m_m_atp_c;m_m_adp_c;ones(1,size(y,2));m_m_glc__D_c],model.rxnParams(1).kineticParams);
v(2,:) = r_R_GLK1([ones(1,size(y,2));m_m_atp_c;m_m_adp_c;m_m_g6p_c],model.rxnParams(2).kineticParams);
v(3,:) = r_R_GLCNt2rpp1([m_m_glcn_p;m_m_glcn_c],model.rxnParams(3).kineticParams);
v(4,:) = r_R_GNK1([m_m_glcn_c;m_m_atp_c;m_m_adp_c;m_m_6pgc_c],[m_m_gthox_c],model.rxnParams(4).kineticParams,model.rxnParams(4).KnegEff,model.rxnParams(4).L,subunits(4));
v(5,:) = r_R_2DHGLCNkt_tpp1([m_m_2dhglcn_p;m_m_2dhglcn_c],model.rxnParams(5).kineticParams);
v(6,:) = r_R_2DHGLCK1([m_m_atp_c;m_m_2dhglcn_c;m_m_6p2dhglcn_c;m_m_adp_c],model.rxnParams(6).kineticParams);
v(7,:) = r_R_PGLCNDH_NAD1([m_m_nadh_c;m_m_6p2dhglcn_c;m_m_nadph_c;m_m_6p2dhglcn_c;m_m_nad_c;m_m_nadp_c;m_m_6pgc_c;m_m_6pgc_c],model.rxnParams(7).kineticParams);
v(8,:) = r_R_PGLCNDH_NADP1([m_m_nadh_c;m_m_6p2dhglcn_c;m_m_nadph_c;m_m_6p2dhglcn_c;m_m_nad_c;m_m_nadp_c;m_m_6pgc_c;m_m_6pgc_c],model.rxnParams(8).kineticParams);
v(9,:) = r_R_GLCDpp1([m_m_glc__D_p;ones(1,size(y,2));m_m_glcn_p;ones(1,size(y,2))],model.rxnParams(9).kineticParams);
v(10,:) = r_R_GAD2ktpp1([ones(1,size(y,2));m_m_glcn_p;m_m_2dhglcn_p;ones(1,size(y,2))],model.rxnParams(10).kineticParams);
v(11,:) = r_R_G6PDH21([m_m_nadp_c;m_m_g6p_c;m_m_6pgl_c;m_m_nadph_c],[m_m_nadph_c;m_m_nadh_c],model.rxnParams(11).kineticParams,model.rxnParams(11).KnegEff,model.rxnParams(11).L,subunits(11));
v(12,:) = r_R_G6PDH2_NAD1([m_m_nad_c;m_m_g6p_c;m_m_nadp_c;m_m_g6p_c;m_m_6pgl_c;m_m_6pgl_c;m_m_nadh_c;m_m_nadph_c],[m_m_nadph_c;m_m_nadh_c],model.rxnParams(12).kineticParams,model.rxnParams(12).KnegEff,model.rxnParams(12).L,subunits(12));
v(13,:) = r_R_G6PDH2_NADP1([m_m_nad_c;m_m_g6p_c;m_m_nadp_c;m_m_g6p_c;m_m_6pgl_c;m_m_6pgl_c;m_m_nadh_c;m_m_nadph_c],[m_m_nadph_c;m_m_nadh_c],model.rxnParams(13).kineticParams,model.rxnParams(13).KnegEff,model.rxnParams(13).L,subunits(13));
v(14,:) = r_R_PGL1([m_m_6pgl_c;m_m_6pgc_c],model.rxnParams(14).kineticParams);
v(15,:) = r_R_GND_NAD1([m_m_6pgc_c;m_m_nad_c;m_m_6pgc_c;m_m_nadp_c;m_m_nadh_c;m_m_nadph_c;m_m_ru5p__D_c;m_m_ru5p__D_c],[m_m_nadph_c],model.rxnParams(15).kineticParams,model.rxnParams(15).KnegEff,model.rxnParams(15).L,subunits(15));
v(16,:) = r_R_GND_NADP1([m_m_6pgc_c;m_m_nad_c;m_m_6pgc_c;m_m_nadp_c;m_m_nadh_c;m_m_nadph_c;m_m_ru5p__D_c;m_m_ru5p__D_c],[m_m_nadph_c],model.rxnParams(16).kineticParams,model.rxnParams(16).KnegEff,model.rxnParams(16).L,subunits(16));
v(17,:) = r_R_RPI1([m_m_ru5p__D_c;m_m_r5p_c],model.rxnParams(17).kineticParams);
v(18,:) = r_R_RPE1([m_m_ru5p__D_c;m_m_xu5p__D_c],model.rxnParams(18).kineticParams);
v(19,:) = r_R_TKT11([m_m_r5p_c;m_m_xu5p__D_c;m_m_g3p_c;m_m_s7p_c],model.rxnParams(19).kineticParams);
v(20,:) = r_R_TKT21([m_m_xu5p__D_c;m_m_e4p_c;m_m_g3p_c;m_m_f6p_c],model.rxnParams(20).kineticParams);
v(21,:) = r_R_TALA1([m_m_s7p_c;m_m_g3p_c;m_m_e4p_c;m_m_f6p_c],model.rxnParams(21).kineticParams);
v(22,:) = r_R_EDD1([m_m_6pgc_c;m_m_2ddg6p_c],[m_m_nadph_c],model.rxnParams(22).kineticParams,model.rxnParams(22).KposEff,model.rxnParams(22).L,subunits(22));
v(23,:) = r_R_EDA1([m_m_2ddg6p_c;m_m_g3p_c;m_m_pyr_c],model.rxnParams(23).kineticParams);
v(24,:) = r_R_PGI1([m_m_g6p_c;m_m_f6p_c],model.rxnParams(24).kineticParams);
v(25,:) = r_R_FBP1([m_m_fdp_c;m_m_f6p_c;ones(1,size(y,2))],model.rxnParams(25).kineticParams);
v(26,:) = r_R_FBA1([m_m_dhap_c;m_m_g3p_c;m_m_fdp_c],model.rxnParams(26).kineticParams);
v(27,:) = r_R_TPI1([m_m_g3p_c;m_m_dhap_c],model.rxnParams(27).kineticParams);
v(28,:) = r_R_GAPD1([m_m_nad_c;m_m_g3p_c;ones(1,size(y,2));m_m_13dpg_c;m_m_nadh_c],[m_m_h2o2_c],model.rxnParams(28).kineticParams,model.rxnParams(28).KnegEff,model.rxnParams(28).L,subunits(28));
v(29,:) = r_R_PGK1([m_m_adp_c;m_m_13dpg_c;m_m_3pg_c;m_m_atp_c],model.rxnParams(29).kineticParams);
v(30,:) = r_R_PGM1([m_m_3pg_c;m_m_2pg_c],model.rxnParams(30).kineticParams);
v(31,:) = r_R_ENO1([m_m_2pg_c;m_m_pep_c],model.rxnParams(31).kineticParams);
v(32,:) = r_R_PYK1([m_m_adp_c;m_m_pep_c;m_m_atp_c;m_m_pyr_c],[m_m_2ddg6p_c;m_m_r5p_c;m_m_f6p_c],model.rxnParams(32).kineticParams,model.rxnParams(32).KposEff,model.rxnParams(32).L,subunits(32));
v(33,:) = r_R_GTHPi1([m_m_h2o2_c;m_m_gthrd_c;m_m_gthox_c;],model.rxnParams(33).kineticParams);
v(34,:) = r_R_GTHOr1([m_m_nadph_c;m_m_gthox_c;m_m_nadp_c;m_m_gthrd_c],model.rxnParams(34).kineticParams);
v(35,:) = r_R_AXPr1(m_m_atp_c,m_m_adp_c,model.rxnParams(35).kineticParams);
v(36,:) = r_R_NADHr1(m_m_nadh_c,m_m_nad_c,model.rxnParams(36).kineticParams);
v(37,:) = r_R_NADPHr1(m_m_nadph_c,m_m_nadp_c,model.rxnParams(37).kineticParams);
v(38,:) = r_R_EX_pyr1(m_m_pyr_c,ones(1,size(y,2)),model.rxnParams(38).kineticParams);
v(39,:) = r_R_EX_pep1(m_m_pep_c,ones(1,size(y,2)),model.rxnParams(39).kineticParams);
v(40,:) = r_R_EX_h2o21(ones(1,size(y,2)),m_m_h2o2_c,model.rxnParams(40).kineticParams);
v(41,:) = r_R_EX_g6p1(m_m_g6p_c,ones(1,size(y,2)),model.rxnParams(41).kineticParams);
v(42,:) = r_R_EX_6pgc1(ones(1,size(y,2)),m_m_6pgc_c,model.rxnParams(42).kineticParams);
v(43,:) = r_R_EX_r5p1(m_m_r5p_c,ones(1,size(y,2)),model.rxnParams(43).kineticParams);
v(44,:) = r_R_EX_xu5p__D1(ones(1,size(y,2)),m_m_xu5p__D_c,model.rxnParams(44).kineticParams);
v(45,:) = r_R_EX_g3p1(m_m_g3p_c,ones(1,size(y,2)),model.rxnParams(45).kineticParams);
v(46,:) = r_R_EX_e4p1(m_m_e4p_c,ones(1,size(y,2)),model.rxnParams(46).kineticParams);
v(47,:) = r_R_EX_f6p1(m_m_f6p_c,ones(1,size(y,2)),model.rxnParams(47).kineticParams);
v(48,:) = r_R_EX_3pg1(m_m_3pg_c,ones(1,size(y,2)),model.rxnParams(48).kineticParams);
v(49,:) = r_R_GLCtex1(ones(1,size(y,2)),m_m_glc__D_p,model.rxnParams(49).kineticParams);

y = (1./(metsRefConc.*10^6)) .* (Sred*(E.*v));