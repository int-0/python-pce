# Introduccion #

La filosofía que intenta seguir PCE es agrupar el contenido de una aventura en una serie de _repositorios_. Esto facilita trabajar con PCE puesto que todos los elementos de una aventura tendrán un repositorio. En este repositorio se podrá trabajar de forma independiente y los cambios en un elemento de un repositorio no afectarán al resto de elementos y repositorios.

# Repositorios en PCE #

Existen dos tipos principales de repositorios: _[stacks](Stacks.md)_ y _[registries](Registries.md)_. La diferencia principal es simple: los elementos de los _stacks_ no tienen ninguna _inteligencia_, en cambio los elementos de un _registry_ tienen cierta _inteligencia_.

La segunda diferencia principal es que un juego en PCE puede tener (y tendrá) muchos _stacks_ del mismo tipo. En cambio sólo podrá tener un único _registry_ para cada tipo.

Normalmente todo el arte de una aventura se almacenará/cargará mediante _stacks_ y los elementos del juego en un _registry_. Esto implica algo evidente: un elemento del juego no sería _visible_ en una aventura si no se relacionase a su vez con un elemento de un _stack_.

## Ejemplo ##

Supongamos un personaje normal y corriente. El objeto PCE que implementa ese personaje estará almacenado en un _registry_. En cambio, todos los fotogramas que permiten dibujar al personaje se almacenarán en un _stack_. Para tener acceso rápido a estos fotogramas através del _objeto personaje_ es necesario tener las referencias de las imágenes dentro del propio objeto del _registry_.

El personaje podrá tener varios _stacks_ de fotogramas según sea necesario (por ejemplo: un _stack_ para cada tipo de atuendo). La aventura tendrá un único _registry_ de actores al que pertenecerá nuestro personaje.