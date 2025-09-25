from enum import Enum

SegmentationCode = Enum('segmentation_code', [
    ('Assistência_Social', 1),
    ('Associações_Patronais_e_Profissionais', 2),
    ('Cultura_e_Recreação', 3),
    ('Desenvolvimento_e_Defesa_de_Direitos_e_Interesses', 4),
    ('Educação_e_Pesquisa', 5),
    ('Outras_Atividades_Associativas', 6),
    ('Religião', 7),
    ('Saúde', 8)
])
