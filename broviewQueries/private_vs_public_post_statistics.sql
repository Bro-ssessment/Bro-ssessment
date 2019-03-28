CREATE VIEW private_vs_public_post_statistics AS
SELECT pub.c_id                                         AS c_id,
       (priv.avg_wc / pub.avg_wc)                       AS private_wc_over_public_wc,
       ((priv.min_wc)::numeric / (pub.min_wc)::numeric) AS priv_min_wc_over_pub_min_wc,
       ((priv.max_wc)::numeric / (pub.max_wc)::numeric) AS priv_max_wc_over_pub_max_wc,
       (priv.avg_bs / pub.avg_bs)                       AS private_bs_over_public_bs,
       (priv.min_bs / pub.min_bs)                       AS priv_min_bs_over_pub_max_bs,
       (priv.max_bs / pub.max_bs)                       AS priv_max_bs_over_pub_max_bs
FROM public_post_statistics pub,
     private_post_statistics priv
WHERE (pub.c_id = priv.c_id);
