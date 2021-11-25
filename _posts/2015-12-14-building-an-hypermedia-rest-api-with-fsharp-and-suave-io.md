---
title: Building an Hypermedia REST API with F# and Suave.IO
tags: fsharp, suaveio, functional_programming, web
---
Hypermedia, also known by the acronym HATEOAS (Hypermedia as the Engine of Application State), is an architecture feature of REST applications that allows clients to fully interact with a service through resources provided dynamically by the server. This enables that client and server implementations can evolve independently.

The way that we are currently generating a service documentation, whether in SOAP services using WSDL or in APIs without Hypermedia, does not make easy the change and any change in the API is capable of breaking all clients which are using it. In some scenarios, where client applications are known and controlled, we can live with this fragility. However, when we are developing a public API that we design for a number of clients that is constantly growing and to be consumed by different devices, it does not seem very appropriate that a change in our API have to break client applications that are already deployed. Hypermedia in the end provides a protection from our API changes on the server.

In this post we will see how we can create a Hypermedia Web API using [Suave.IO](http://suave.io/) and F#. I’ll start from the example of WebAPI that wrote Tamizhvendan few months ago. Here you have an introduction to development with Suave.IO and a complete explanation in this [entry](http://blog.tamizhvendan.in/blog/2015/06/11/building-rest-api-in-fsharp-using-suave/) on his blog.

Basically, for putting it into context, the solution consists in a F# Console Application project with two modules (Db and RestFul). Then we have added the nuget references to **Suave.IO** and **Newtonsoft.Json** packages.

The DB module provides a dictionary in memory to store contacts details. Here we can see the full implementation of this module.

    namespace SuaveRestApi.Db
    
    open System.Collections.Generic
    
    type Person = {
      Id : int
      Name : string
      Age : int
      Email : string
    }
    
    module Db =        
    
      let peopleStorage = new Dictionary<int, Person>()
      let getPeople () = 
          peopleStorage.Values |> Seq.map (fun p -> p)
      let getPerson id =
          if peopleStorage.ContainsKey(id) then
              Some peopleStorage.[id]
          else
              None
      let createPerson person =
          let id = peopleStorage.Values.Count + 1
          let newPerson = {
              Id = id
              Name = person.Name
              Age = person.Age
              Email = person.Email
          }
          peopleStorage.Add(id, newPerson)
          newPerson    
    
      let updatePersonById personId personToBeUpdated =
          if peopleStorage.ContainsKey(personId) then
              let updatedPerson = {
                  Id = personId
                  Name = personToBeUpdated.Name
                  Age = personToBeUpdated.Age
                  Email = personToBeUpdated.Email
              }
              peopleStorage.[personId] <- updatedPerson
                  
              Some updatedPerson
          else 
              None
    
      let updatePerson personToBeUpdated =
          updatePersonById personToBeUpdated.Id personToBeUpdated 
    
      let deletePerson personId = 
          peopleStorage.Remove(personId) |> ignore
    
      let isPersonExists  = peopleStorage.ContainsKey
    

The module RestFul contains the type RestResource representing all operations that can be performed on a restful resource abstracting the real resource from the REST API Web Part.

    type RestResource<'a> = {
      GetAll : unit -> 'a seq
      GetById : int -> 'a option
      IsExists : int -> bool
      Create : 'a -> 'a
      Update : 'a -> 'a option
      UpdateById : int -> 'a -> 'a option
      Delete : int -> unit
    }
    

The main function of this module, the rest function, returns the Web Part constructed from the name of the resource and RestResource.

    let rest resourceName resource =
      
        …    
    
        choose [
                path resourcePath >>= choose [
                    GET >>= getAll
                    POST >>= request (getResourceFromReq >> resource.Create >> JSON)
                    PUT >>= request (getResourceFromReq >> resource.Update >> handleResource badRequest)
                ]
                DELETE >>= pathScan resourceIdPath deleteResourceById
                GET >>= pathScan resourceIdPath getResourceById
                PUT >>= pathScan resourceIdPath updateResourceById
                HEAD >>= pathScan resourceIdPath isResourceExists
            ]
    

Adding Hypermedia
-----------------

Now that we have presented the actors, if we execute the application, we can see that this application only returns information about the contacts. **The idea behind Hypermedia is that, in addition to data, the Hypermedia artifacts offer to clients a set of actions or operation that can be performed at a given time**. That is, for instance, that the response should show if an operation on a resource is available in a particular state. In applications using no Hypermedia APIs, much of this logic is moving to the client. Suppose we add to the previous API a new functionality that adds a contact as a favorite. The API should return the details of how to make the request and that information should come only if the contact is not already added as a favorite, otherwise, the API should return how to remove it from favorites.

In order to standardize the response and structure of our API, we can use different types of Hypermedia formats: **JSON-LD**, **HAL**, **Collection+JSON**, etc. For this first example, I will use the format Collection+JSON, a Hypermedia type that standardizes reading, writing and querying simple collections. [Here](http://amundsen.com/media-types/collection/) are available information about Collection+JSON Hypermedia Type.

To start we will implement the minimum representation of a document Collection+JSON that consists in returning a collection object with two properties, version and a URI that points to the resource itself.

    { "collection" : 
      {
         "version" : "1.0",
         "href" : "http://example.org/people/"
      } 
    }
    

We start by creating a new type in the Restful module that we will use to store version and URI.

    type Collection = {
      Version : string
      Href : string
    }
    

And a new type generated by composition using Collection type.

    type Resource = {
        Collection: Collection
    }
    

So we can use this new type, we have to change the type for the input type that is different from the output type.

    type RestResource<'a,'b> = {
      GetAll : unit -> 'b seq
      GetById : int -> 'b option
      IsExists : int -> bool
      Create : 'a -> 'b
      Update : 'a -> 'b option
      UpdateById : int -> 'a -> 'b option
      Delete : int -> unit
    }
    

We create the function getCollection that we use to return the Resource type information.

    let getCollection resource =
      let collection = { Version = "1.0"; Href = host + resourcePath }
      collection
    

And to test this implementation, we modify the function _handleResource_ to add the call to the function and return getCollection Hypermedia links in the response.

    let handleResource requestError = function
       | Some r -> r |> getCollection |> JSON
       | _ -> requestError
    

If now we make a request for information from a contact, we obtain the following information:

![postman-get](/img/postman-get.png)

As example it’s a bit weird, because we’re not showing anything about the resource. To fix this we will return a Collection+JSON Document which contains one or more item objects in an array. The response may describe all, or only a partial list, of the items in a collection.

First step is to create the new types to store Item data and to add a new Item sequence property to the Collection type.

    type Data = {
      Name : string
      Value : string
    }
    
    type Item = {
      Href: string
      Data: Data list
    }
    
    type Collection = {
      Version : string
      Href : string
      Items : Item seq
    }
    

And then we need to modify the getCollection function to add the value of Items property.

    let getCollection items =
      let href = host + resourcePath + "/"
      let collection = { Version = "1.0"; Href = href; Items = items }
      { Collection = collection }
    

And finally, we need to add the new two functions to generate the sequence of Items and Data properties.

    let getData person = 
      [ { Name  = "Id"; Value = string person.Id } 
        { Name  = "Name"; Value = person.Name } 
        { Name  = "Age"; Value = string person.Age }
        { Name  = "Email"; Value = person.Email } ]
    
    let getItems resource =
        resource |> Seq.map (fun p -> { Href= url + string p.Id; Data = p |> getData } )
    

Now, if we make the same request we made in the previous step, we get the following response:

![postman-get-full](/img/postman-get-full.png)

This is a very simple example to modify our API to return additional information. Basically all changes have been made using new types and by composing functions. In upcoming posts I will continue adding new examples and generalizing the implementation so that it can be easily reusable.

Summary
-------

In this post I made a first approach to the development of Hypermedia APIs with Suave.IO and F#, making our APIs provide documentation and are self-discoverable while we make them more flexible to changes, while protecting clients of those same changes at the same time they are decoupled from the server workflow.

Resources
---------

[Building REST Api in Fsharp Using Suave](http://blog.tamizhvendan.in/blog/2015/06/11/building-rest-api-in-fsharp-using-suave/)  
[Collection+JSON - Hypermedia Type](http://amundsen.com/media-types/collection/)  
[On choosing a hypermedia type for your API - HAL, JSON-LD, Collection+JSON, SIREN, Oh My!](http://sookocheff.com/post/api/on-choosing-a-hypermedia-format/)

