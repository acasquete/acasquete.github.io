---
title: Notificaciones Toast programadas en aplicaciones Metro
tags: [windows_store]
---
Las notificaciones de sistema o _Toast_ son los mensajes que aparecen en la esquina de la pantalla y que pueden ir acompañados de una imagen, texto y sonido. Lo más interesante de este tipo de notificaciones es que se muestran aunque la aplicación no esté en ejecución. Esto quiere decir que la aplicación puede programar una serie de notificaciones para que se muestren en una horas determinadas. Además es posible enviar una notificación a través de Windows Push Notification Services (WNS). En este primer articulo vamos a ver los conceptos básicos y cómo crear notificaciones programadas y dejaremos para la segunda parte, el escenario realmente interesante, enviar las notificaciones Push desde nuestro servicio en Windows Azure.

Comenzamos creando el objeto **ToastNotifier** que se encargará de programar las notificaciones, este objeto se instancia mediante el método **createToastNotifier** de la clase **Windows.UI.Notifications.ToastNotificationManager**.

var toast = Windows.UI.Notifications; var notifier = toast.ToastNotificationManager.createToastNotifier();</pre> Es importante comprobar si las notificaciones están activadas, ya que el usuario o un administrador vía políticas de grupo pueden deshabilitar el uso de notificaciones desde el panel de control a nivel general de todo el sistema operativo o por aplicación. En caso de tener habilitadas las notificaciones la propiedad setting tendrá el valor **enabled**, y en caso contrario el motivo por el que no lo están (bloqueado por aplicación, por usuario, por políticas de grupo o por manifiesto).

if (notifier.setting != toast.NotificationSetting.enabled) {
    var dialog = new Windows.UI.Popups.MessageDialog("Las notificaciones no están habilitadas.");
    dialog.showAsync();
    return;
}

Las notificaciones _Toast_, al igual que las Tiles, están basadas en plantillas XML. Mediante el método **GetTemplateContent** podemos obtener el contenido XML para poder personalizarlo. Este método necesita que Indiquemos la plantilla mediante un valor de la enumeración **ToastTemplateType**. Hay disponibles 8 plantillas que combinan imágenes y texto. Todos los tipos de plantillas disponibles se pueden ver en la [ayuda sobre ToastTemplateType en la MSDN](http://msdn.microsoft.com/en-us/library/windows/apps/windows.ui.notifications.toasttemplatetype).

var templateXml = toast.ToastNotificationManager.getTemplateContent(toast.ToastTemplateType.toastImageAndText04);

Este método devuelve un objeto XmlDocument que debemos personalizar modificando el contenido y el texto. En el siguiente ejemplo la plantilla modificamos el primer elemento de tipo **text**.

var textElements = templateXml.getElementsByTagName("text");
element\[0\].appendChild(template.createTextNode("Recordatorio evento SNUG!"));

Sin embargo, algunas plantillas pueden contener varios elementos de texto o imagenes. Por ejemplo, la plantilla **toastImageAndText04** que contiene una imagen y tres líneas de texto. En el siguiente código se establece el contenido de la imagen y de los tres elementos de texto.

// Imagen
var imageElements = templateXml.getElementsByTagName("image");
imageElements\[0\].setAttribute("src", "ms-appx:///images/win8startscreen.jpg");

// Texto
var element = templateXml.getElementsByTagName("text");
element\[0\].appendChild(templateXml.createTextNode("Recordatorio Evento SNUG!"));
element\[1\].appendChild(templateXml.createTextNode("Aplicaciones Metro para Desarrolladores Web"));
element\[2\].appendChild(templateXml.createTextNode("Martes, 10 de julio"));

También es posible especificar un sonido que se reproduzca cuando se muestre la notificación. Simplemente tenemos que crear un elemento **audio** y como source de este elemento indicar un sonido del sistema mediante alguno de estos valores: alguno de estos valores: Notification.Default, Notification.IM, Notification.Mail, Notification.Reminder, Notification.SMS, Notification.Looping.Alarm, Notification.Looping.Alarm2, Notification.Looping.Call, Notification.Looping.Call2. Los cinco primeros son sonidos que se reproducen una sola vez y no se repiten, y el resto son sonidos a los que podemos indicar que se repitan, asignando el atributo **loop**. En el siguiente ejemplo se muestra como crear el elemento **audio**para que se reproduzca indefinidamente hasta que el usuario pulse en la notificación.

var toastNode = templateXml.selectSingleNode("/toast");
var audioElement = templateXml.createElement("audio");
audioElement.setAttribute("src", "ms-winsoundevent:Notification.Looping.Call");
audioElement.setAttribute("loop", "true");
toastNode.setAttribute("duration", "long");
toastNode.appendChild(audioElement);

Si queremos que no se reproduzca el sonido podemos establecer el valor del atributo **silent** a **true**.

Ya por último, si queremos que al pulsar sobre la notificación se lance nuestra aplicación tenemos que especificar los argumentos que queremos pasar en el atributo launch. En el siguiente código se muestra cómo hacerlo.

templateXml.selectSingleNode("/toast").setAttribute("launch", '{"type":"toast","parameter1":"12345"}');

Una vez tengamos la plantilla personalizada, sólo tenemos que programar la notificación para una fecha determinada mediante el método **ScheduledToastNotification**. A este método le pasamos la plantilla y la fecha la que queremos mostrar y la añadimos a la colecció de notificaciones programadas mediante el método **addToSchedule**.

En el siguiente código especificamos la fecha actual más 10 segundos.

var date = new Date(new Date().getTime() + 10000);
var stn = toast.ScheduledToastNotification(template, date);
notifier.addToSchedule(stn);

El código completo del módulo es el siguiente, en el que se define el espacio de nombres **notifications** y el método **scheduleToast**.

(function () {
    "use strict";

    var toast = Windows.UI.Notifications;

    WinJS.Namespace.define("notifications", {

        scheduleToast: function () {

            var notifier = toast.ToastNotificationManager.createToastNotifier();

            if (notifier.setting != toast.NotificationSetting.enabled) {
                new Windows.UI.Popups.MessageDialog("Las notificaciones están deshabilitadas").showAsync();
                return;
            }

            var templateXml = toast.ToastNotificationManager.getTemplateContent(toast.ToastTemplateType.toastImageAndText04);

            // Imagen
            var imageElements = templateXml.getElementsByTagName("image");
            imageElements\[0\].setAttribute("src", "ms-appx:///images/win8startscreen.jpg");

            // Texto
            var element = templateXml.getElementsByTagName("text");
            element\[0\].appendChild(templateXml.createTextNode("Recordatorio Evento SNUG"));
            element\[1\].appendChild(templateXml.createTextNode("Aplicaciones Metro para Desarrolladores Web"));
            element\[2\].appendChild(templateXml.createTextNode("Martes, 10 de julio"));

            // Sonido
            var toastNode = templateXml.selectSingleNode("/toast");
            var audioElement = templateXml.createElement("audio");
            audioElement.setAttribute("src", "ms-winsoundevent:Notification.Looping.Call");
            audioElement.setAttribute("loop", "true");
            toastNode.setAttribute("duration", "long");
            toastNode.appendChild(audioElement);

            // Parámetros
            templateXml.selectSingleNode("/toast").setAttribute("launch", '{"type":"toast","parameter1":"12345"}');

            // Programación
            var date = new Date(new Date().getTime() + 3000);
            var stn = toast.ScheduledToastNotification(templateXml, date);
            notifier.addToSchedule(stn);
        }
    });
})();

El único cambio que queda por hacer es modificar el manifiesto de la aplicación para indicar que la aplicación puede enviar y recibir notificaciones. Para indicar esta capacidad, abrimos el fichero appmanifest.xml y marcamos la casilla Capacidad de aviso (\*Toast Capable\*) en la pestaña Application UI. Desde esta pestaña se puede indicar el color de fondo, que es el mismo que el de la pantalla de presentación (\*splash screen\*), el color del texto y la imagen del logotipo pequeño que aparece en la esquina de la notificación.

Hasta aquí esta entrada en la que hemos visto cómo programar notificaciones del sistema, en el siguiente artículo veremos como utilizar las notificaciones Push desde un servicio en Windows Azure.


Referencias
---

[Instrucciones y lista de comprobación de notificaciones del sistema](http://msdn.microsoft.com/es-es/library/windows/apps/hh465391.aspx) 
[Toast notification overview (Metro style apps)](http://msdn.microsoft.com/es-es/library/windows/apps/hh779727.aspx)

