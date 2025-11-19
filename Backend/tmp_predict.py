from texto.predictor import get_predictor

texts = [
"""Este libro ha sido escrito por una personalidad llamada Seth que se describe a sí misma como una
«esencia de energía de la personalidad» que ya no tiene forma física. Durante más de siete años ha hablado a
través de mí en sesiones de trance dos veces a la semana. Mi iniciación psíquica empezó realmente una noche
de septiembre de 1963 cuando estaba sentada escribiendo poesía. De repente, mi consciencia abandonó mi
cuerpo y mi mente fue invadida por un aluvión de ideas sorprendentes y nuevas para mí en esa época. Cuando
volví a mi cuerpo, descubrí que mi mano había producido una escritura automática que explicaba muchos de
los conceptos que me habían sido dados. Incluso había puesto un título a esas notas: «El universo físico como
la interpretación de una idea.»""",
"""Durante más de siete años Seth ha hablado a través de mí en sesiones de trance dos veces a la
semana. Mi iniciación psíquica empezó realmente una noche de septiembre de 1963 cuando estaba sentada
escribiendo poesía. De repente, mi consciencia abandonó mi cuerpo y mi mente fue invadida por un aluvión de
ideas sorprendentes y nuevas para mí en esa época. Cuando volví a mi cuerpo descubrí que mi mano había
producido una escritura automática que explicaba muchos de los conceptos que me habían sido dados. Incluso
había puesto un título a esas notas: "El universo físico como la interpretación de una idea".
No es mi intención insinuar que poseemos la piedra angular de la verdad, o dar la impresión de que
esperamos impacientemente conocer secretos no distorsionados sobre las eras por venir. Sé que todo el
mundo tiene acceso al conocimiento intuitivo y puede obtener atisbos de la realidad interna. El universo nos
habla a cada uno de nosotros a este respecto; en nuestro caso, lo hace a través de las sesiones de Seth."""
]

p = get_predictor('B')
print('Predictor info:', p.get_model_info())
for i, t in enumerate(texts, 1):
    res = p.predict(t)
    print(f'--- Texto {i} ---')
    print(res)
