# Архангельское месторождение, книга 1
from os.path import join

content_a1 = [
    (43, 47, 0),
    (48, 49, 1),
    (50, 67, 2),
    (68, 78, 3),
    (79, 102, 4),
    (103, 181, 5),
    (182, 286, 6),
    (287, 293, 7)
]
# Архангельское месторождение, книга 2
content_a2 = [
    (12, 62, 8),
    (63, 72, 9),
    (73, 79, 10),
    (80, 105, 11.1),
    (106, 152, 11.2),
    (153, 167, 12),
    (168, 228, 13)
]
# Ивинское месторождение, книга 1
content_i1 = [
    (31, 33, 0),
    (34, 36, 1),
    (37, 143, 2),
    (144, 196, 3),
    (197, 276, 4),
    (277, 289, 5),
    (290, 308, 6),
    (309, 335, 7),
    (336, 349, 8),
    (350, 381, 9),
    (382, 407, 10),
    (408, 419, 11),
    (420, 431, 12),
    (432, 454, 13),
    (455, 459, 14)
]
# Щербеньское, книга 1
content_sh1 = [
    (14, 15, 0),
    (16, 18, 1),
    (19, 63, 2),
    (64, 80, 3),
    (81, 97, 4),
    (98, 124, 5),
    (125, 130, 6),
    (131, 151, 7),
    (152, 158, 8),
    (159, 178, 9),
    (179, 196, 10),
    (197, 206, 11),
    (207, 217, 12),
    (218, 237, 13),
    (238, 247, 14)
]
# Байданкинское, книга 1
content_b1 = [
    (33, 35, 0),
    (36, 38, 1),
    (39, 79, 2.1),
    (80, 100, 2.2),
    (101, 136, 2.3),
    (137, 169, 3),
    (170, 232, 4),
    (233, 246, 5)
]
# Байданкинское, книга 2
content_b2 = [
    (8, 18, 6),
    (19, 41, 7),
    (42, 79, 8.1),
    (80, 100, 8.2),
    (101, 119, 8.3),
    (120, 139, 8.4),
    (140, 159, 8.5),
    (160, 179, 8.6),
    (180, 199, 8.7),
    (200, 236, 8.8),
    (237, 263, 9),
    (264, 279, 10),
    (280, 288, 11),
    (289, 295, 12),
    (296, 310, 13),
    (311, 311, 14)
]
# Аканское
content_ac = [
    (19, 21, 0),
    (22, 44, 1),
    (45, 55, 2),
    (56, 105, 3),
    (106, 170, 4),
    (171, 187, 5),
    (188, 189, 6)
]
# Граничное, книга 1
content_g1 = [
    (26, 28, 0),
    (29, 31, 1),
    (32, 60, 2.1),
    (61, 101, 2.2),
    (102, 142, 2.3),
    (143, 184, 3),
    (185, 235, 4),
    (236, 252, 5)
]
# Граничное, книга 2
content_g2 = [
    (10, 25, 6),
    (26, 49, 7.1),
    (50, 64, 7.2),
    (65, 79, 7.3),
    (80, 94, 7.4),
    (95, 109, 7.5),
    (110, 124, 7.6),
    (125, 134, 7.7),
    (135, 150, 8),
    (151, 175, 9),
    (176, 201, 10),
    (202, 213, 11),
    (214, 228, 12),
    (229, 254, 13),
    (255, 256, 14)
]
content_m = [
    (0, 0, '0and16'),
    (0, 0, '1-2'),
    (0, 0, 3),
    (0, 0, 4.1),
    (0, 0, 4.2),
    (0, 0, 5),
    (0, 0, 6),
    (0, 0, 7),
    (0, 0, 8),
    (0, 0, 9),
    (0, 0, 10),
    (0, 0, 11),
    (0, 0, 12),
    (0, 0, '13-15')
]
content_a1_d = [
    (25, 26, 0),
    (27, 29, 1),
    (30, 66, 2.1),
    (67, 129, 2.2),
    (130, 178, 2.3),
    (179, 199, 3.1),
    (200, 262, 3.2),
    (263, 277, 3.3)
]
# полное содержание
REPORTS_FOR_THE_TEST = {
    'content_a1': content_a1,
    'content_a2': content_a2,
    'content_i1': content_i1,
    'content_sh1': content_sh1,
    'content_b1': content_b1,
    'content_b2': content_b2,
    'content_ac1': content_ac,
    'content_g1': content_g1,
    'content_g2': content_g2,
    'content_m': content_m,
    'content_a1_d': content_a1_d
}

PATHS_FOR_REPORTS_PDF = {
    'path_a1': '../reports/pdfs/Архангельское_месторождение_Пересчет_запасов_КГ.pdf',
    'path_a2': '../reports/pdfs/Кн.2_Отчёт Архангельское_ПЕЧАТЬ.pdf',
    'path_i1': '../reports/pdfs/Ивинское, книга 1.pdf',
    'path_sh1': '../reports/pdfs/Книга 1 - Щербеньское.pdf',
    'path_g1': '../reports/pdfs/Том 1 Граничное.pdf',
    'path_g2': '../reports/pdfs/2 Граничное.pdf',
    'path_b1': '../reports/pdfs/Книга 1 - Байданкинское.pdf',
    'path_b2': '../reports/pdfs/Книга 2 - Байданкинское.pdf',
    'path_ac': '../reports/pdfs/Отчет_Аканское месторождение.pdf',
    'path_a1_d': '../reports/pdfs/Текст_отчета_2021_Том_1.pdf'
}

PATHS_FOR_REPORTS_TXT = {
    'path_a1': '../reports/txt/archangelsk',
    'path_a2': '../reports/txt/archangelsk',
    'path_i1': '../reports/txt/ivinskoe',
    'path_sh1': '../reports/txt/sherbenskoe',
    'path_g1': '../reports/txt/granichnoe',
    'path_g2': '../reports/txt/granichnoe',
    'path_b1': '../reports/txt/baydankinskoe',
    'path_b2': '../reports/txt/baydankinskoe',
    'path_ac': '../reports/txt/acanskoe',
    'path_m': '../reports/txt/matrosovskoe',
    'path_a1_d': '../reports/txt/archangelsk_d'
}

CONTENT_A1 = [i[2] for i in content_a1]
CONTENT_A2 = [i[2] for i in content_a2]
CONTENT_I = [i[2] for i in content_i1]
CONTENT_SH = [i[2] for i in content_sh1]
CONTENT_B1 = [i[2] for i in content_b1]
CONTENT_B2 = [i[2] for i in content_b2]
CONTENT_AC = [i[2] for i in content_ac]
CONTENT_G1 = [i[2] for i in content_g1]
CONTENT_G2 = [i[2] for i in content_g2]
CONTENT_M = [i[2] for i in content_m]
CONTENT_A1_D = [i[2] for i in content_a1_d]

CONTENTS = {
    'content_a1': CONTENT_A1,
    'content_a2': CONTENT_A2,
    'content_i1': CONTENT_I,
    'content_sh1': CONTENT_SH,
    'content_b1': CONTENT_B1,
    'content_b2': CONTENT_B2,
    'content_ac1': CONTENT_AC,
    'content_g1': CONTENT_G1,
    'content_g2': CONTENT_G2,
    'content_m': CONTENT_M,
    'content_a1_d': CONTENT_A1_D
}
path_to_docx_m = join(
    'D:\\For_Python',
    'Unstructured-field-data-aggregator',
    'reports',
    'docx',
    'matrosovskoe'
)

path_to_docx_a = join(
    'D:\\For_Python',
    'Unstructured-field-data-aggregator',
    'reports',
    'docx',
    'archangelsk_d'
)

DOCX_PATHS = {
    'matrosovskoe': path_to_docx_m,
    'archangelsk_d': path_to_docx_a
}

DOCX_PATHS_M = [
    'инф. справка, введение, заключение.docx',
    'Гл. 1,2-геология.doc',
    'Глава 3.docx',
    'Отчет по геологической модели.docx',
    'Отчёт по гидродинамике.docx',
    'Глава 5.doc',
    'Глава 6 Матросовское.doc',
    'Глава 7.docx',
    'Глава 8.docx',
    'Глава 9.docx',
    'Глава 10.docx',
    'Гл. 11-контроль.doc',
    'Гл. 12-доразведка.doc',
    'Главы 13,14,15.doc'
]
DOCX_PATHS_A = [
    'Текст_отчета_2021_Том_1.docx'
]

DOCX_CHAPTERS_PATHS = {
    'matrosovskoe': DOCX_PATHS_M,
    'archangelsk_d': DOCX_PATHS_A
}

CONTENT_DOCX_M = [
    (2, 3, 0, join(path_to_docx_m, 'инф. справка, введение, заключение.docx')),
    (1, 3, 1, join(path_to_docx_m, 'Гл. 1,2-геология.doc')),
    (4, 57, 2, join(path_to_docx_m, 'Гл. 1,2-геология.doc')),
    (1, 11, 3, join(path_to_docx_m, 'Глава 3.docx')),
    (1, 11, 4.1, join(path_to_docx_m, 'Отчет по геологической модели.docx')),
    (1, 6, 4.2, join(path_to_docx_m, 'Отчёт по гидродинамике.docx')),
    (1, 5, 5, join(path_to_docx_m, 'Глава 5.doc')),
    (1, 9, 6, join(path_to_docx_m, 'Глава 6 Матросовское.doc')),
    (1, 18, 7, join(path_to_docx_m, 'Глава 7.docx')),
    (1, 12, 8, join(path_to_docx_m, 'Глава 8.docx')),
    (1, 11, 9, join(path_to_docx_m, 'Глава 9.docx')),
    (1, 19, 10, join(path_to_docx_m, 'Глава 10.docx')),
    (1, 11, 11, join(path_to_docx_m, 'Гл. 11-контроль.doc')),
    (1, 14, 12, join(path_to_docx_m, 'Гл. 12-доразведка.doc')),
    (1, 8, 13, join(path_to_docx_m, 'Главы 13,14,15.doc')),
    (9, 50, 14, join(path_to_docx_m, 'Главы 13,14,15.doc')),
    (51, 55, 15, join(path_to_docx_m, 'Главы 13,14,15.doc')),
    (4, 5, 16, join(path_to_docx_m, 'инф. справка, введение, заключение.docx'))
]

CONTENTS_DOCX = {
    'matrosovskoe': CONTENT_DOCX_M
}
