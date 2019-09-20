-- SMAP Weights normalization

select * from weights_elements_c;
select * from weights_categories_c;
select * from module_personas_c;

-- Checking all e_weights + price_score_weights sum %100
select *, sum_weight + price_score_weight from (
	select m_id, persona_id, sum(weight) as sum_weight from weights_categories_c group by m_id, persona_id
    ) t1
    join module_personas_c on t1.m_id = module_personas_c.m_id and t1.persona_id = module_personas_c.persona_id;
    
Select * from sum_e_weight_by_c;
CREATE OR REPLACE VIEW sum_e_weight_by_c AS
	SELECT t1.m_id, t1.persona_id, t1.c_id, t1.sum_e_weight_by_c, weights_categories_c.c_weight
    FROM (
		SELECT weights_elements_c.m_id, weights_elements_c.persona_id, weights_categories_c.c_id, sum(e_weight) as sum_e_weight_by_c
		FROM weights_elements_c
		LEFT JOIN elements_c on weights_elements_c.e_id = elements_c.eid 
		LEFT JOIN subcategories_c on elements_c.s_id = subcategories_c.sid
		LEFT JOIN weights_categories_c ON weights_elements_c.m_id = weights_categories_c.m_id AND weights_elements_c.persona_id = weights_categories_c.persona_id AND subcategories_c.c_id = weights_categories_c.c_id
		GROUP BY weights_elements_c.m_id, weights_elements_c.persona_id, weights_categories_c.c_id
	) t1
    LEFT JOIN weights_categories_c ON t1.m_id = weights_categories_c.m_id AND t1.persona_id = weights_categories_c.persona_id AND t1.c_id = weights_categories_c.c_id;

select * from norm_e_weights;
CREATE OR REPLACE VIEW norm_e_weights AS
	SELECT weights_elements_c.m_id, weights_elements_c.persona_id, weights_elements_c.e_id,
	sum_e_weight_by_c.c_id, sum_e_weight_by_c.sum_e_weight_by_c, sum_e_weight_by_c.c_weight,
	e_weight/sum_e_weight_by_c*c_weight as norm_weight
	FROM weights_elements_c
	LEFT JOIN elements_c on weights_elements_c.e_id = elements_c.eid 
	LEFT JOIN subcategories_c on elements_c.s_id = subcategories_c.sid
	LEFT JOIN sum_e_weight_by_c ON weights_elements_c.m_id = sum_e_weight_by_c.m_id AND weights_elements_c.persona_id = sum_e_weight_by_c.persona_id AND subcategories_c.c_id = sum_e_weight_by_c.c_id;

select *, sum_norm_weights + price_score_weight from (    
	select norm_e_weights.m_id, norm_e_weights.persona_id, sum(norm_weight) as sum_norm_weights from norm_e_weights group by m_id, persona_id
    ) t1
    join module_personas_c on t1.m_id = module_personas_c.m_id and t1.persona_id = module_personas_c.persona_id;