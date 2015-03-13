# Stacks #

Como ya se ha explicado, los _stacks_ almacenan todo el contenido _multimedia_ de una aventura PCE. Por tanto, utilizaremos los _stacks_ para cargar los gráficos y los sonidos de una aventura.

Aunque en esencia sean lo mismo, la forma de utilizarlo es muy diferente según el tipo de elemento que almacenen.

> Evidentemente este diseño podría resultar _inadecuado_ desde el punto de    vista de la programación orientada a objetos, pero no hay que olvidar que pretendemos crear un programa capaz de correr más o menos rápido en máquinas normales. Utilizar un lenguaje interpretado ya supone suficiente penalización de velocidad como para estar creando jerarquías de herencias de muchos niveles.

Así pues distinguimos tres tipos de _stacks_:

  * _[SoundStack](Stacks#SoundStack.md)_
  * _[FrameStack](Stacks#FrameStack.md)_
  * _[AnimationStack](Stacks#AnimationStack.md)_

El primer tipo maneja todos los fotogramas usados por los elementos de los _registers_. El segundo almacena todos los efectos de sonido. Por razones de simplicidad y eficiencia, es recomendable usar un único _SoundStack_ por escena. En cambio, aunque suponga una penalización en el consumo de memoria, será recomendable usar varios _FrameStack_ por cada elemento de la escena.

## SoundStack ##

A diferencia de los _FrameStack_, los _SoundStack_ no sólo almacenan fotogramas, también permiten usar los sonidos que almacenan.

Un objeto _SoundStack_ permite cargar los sonidos que se deseen. Estos se cargan como objetos _pygame_ adecuados y se indexan mediante un identificador (una cadena). El _stack_ permite reproducir un sonido una vez o como un bucle infinito. En este último caso se retorna un identificador para permitir parar este sonido cuando se desee.

Además, un _SoundStack_ puede registrarse en un _canal de eventos_ y puede recibir eventos para reproducir/parar la reproducción de sonidos.

Gracias a esto toda la funcionalidad de un _SoundStack_ puede utilizarse de dos formas distintas:
  * Mediante el propio código del programa.
  * En tiempo de ejecución mediante _eventos_.

## FrameStack ##

Los _FrameStack_ se utilizan para cargar directamente los fotogramas de un elemento de la aventura. Los fotogramas se almacenan dentro del _FrameStack_ como grupos de imágenes.

Para cargar automáticamente un grupo de imagenes, éstas deben tener el mismo nombre pero con una terminación numérica diferente, por ejemplo: _frame01.png, frame02.png, frame03.png_ podrían cargarse de una sóla vez como un grupo dentro del _FrameStack_. Cuando se carga un grupo se le da un nombre que servirá para identificar el grupo.

Una vez que hemos cargado un grupo, podemos realizar ciertas operaciones que nos serán de utilidad: duplicar el grupo (crea un grupo idéntico al origen pero con otro nombre), espejar horizontalmente las imágenes del grupo, espejar verticalmente las imágenes del grupo y por último aplicar un factor de escala a cada imagen del grupo. Estas utilidades nos permitirán precalcular todas las imágenes necesarias en lugar de tener que crear archivos de imágenes para todos los tamaños de un objeto móvil.

## AnimationStack ##

A partir de los grupos almacenados en un _FrameStack_ podremos crear nuestras animaciones.

Como los fotogramas ya están almacenados en el _FrameStack_, en el _AnimationStack_ no se guardan otra vez, simplemente contiene vectores con índices a los grupos. Además, podremos intercambiar el _FrameStack_ de un _AnimationStack_, esto podría permitir tener un único juego de animaciones para todas las posibles representaciones de un personaje, por ejemplo.

Cuando tenemos un _AnimationStack_ podremos crear tres tipos de animaciones lineales a partir de un grupo en un _FrameStack_:
  * Loop (secuencia lineal de los fotogramas de un grupo)
  * Ping-pong (generado a partir de un loop)
  * Inversa (fotogramas en orden contrario)

Cada animación dentro de un _AnimationStack_ también será referenciado por su nombre.

En PCE, todos los elementos dibujables (o _Drawables_) se crean a partir de un _AnimationStack_.