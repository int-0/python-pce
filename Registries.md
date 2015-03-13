# Registries #

Para simplificar el diseño de aventuras con PCE, todos los elementos _inteligentes_ o _interactivos_ de un proyecto se almacenan en _registries_. Esto implica que en todo momento, el _estado_ del juego se resume en el estado de estos _registries_.

Los _registry_ son únicos, es decir: existe un único _registry_ de cada tipo para todo el juego. Para ello son implementados usando el patrón _singleton_.

Cada _registry_ tiene un _canal de eventos_ interno que se usa para la comunicación entre los propios elementos del _registry_. Además es capaz de recibir eventos, pero no los procesa, simplemente se reenvían por el canal interno (_event forwarding_).

Las operaciones de añadir/eliminar elementos de un _registry_ se realizan de forma estática en el momento de la creación del juego. Esto implica que el número de elementos de un _registry_ a lo largo de todo el juego permanecerá constante (aunque podría forzarse el crear/eliminar elementos).

Actualmente estos son los tipos de _registries_ creados en PCE:

  * _ItemRegistry_
  * _ActorRegistry_