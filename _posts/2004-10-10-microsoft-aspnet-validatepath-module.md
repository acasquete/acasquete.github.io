---
title: Microsoft ASP.NET ValidatePath Module
---
Microsoft has released an [ASP.NET HTTP module](http://www.microsoft.com/downloads/details.aspx?FamilyId=DA77B852-DFA0-4631-AAF9-8BCC6C743026&displaylang=en) that Web site administrators can apply to their Web server. This module will protect all ASP.NET applications against all potential canonicalization problems known to Microsoft.  
  
Very recommended to avoid the problems of the vulnerability associated with canonicalization!!!  
  
Another solution for this vulnerability is to add the following code to the **global.asax**:  

``` csharp
void Application_BeginRequest(object source, EventArgs e)  
{  
    if (Request.Path.IndexOf('\\') >= 0  
System.IO.Path.GetFullPath(Request.PhysicalPath) != Request.PhysicalPath)  
    {  
        throw new HttpException(404, "not found");  
    }  
}
```
  