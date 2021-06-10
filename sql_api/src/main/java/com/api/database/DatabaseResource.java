package com.api.database;

import javax.ws.rs.*;
import javax.ws.rs.core.Response;

import com.api.connection.SqlServer;
import com.api.connection.LoginHelper;
import com.google.gson.Gson;

import java.util.List;

@Path("/sqlserver")
public class DatabaseResource {

    @GET
    @Path("/test")
    @Produces("application/json")
    public String test(){
        return "SQLServer API up";
    }

    @GET
    @Path("/getAllEmployees")
    @Produces("application/json")
    public String getEmployees() {
        SqlServer sql = new SqlServer();
        List<String> names_ = sql.getNames();

        Gson gson = new Gson();
        return gson.toJson(names_);
    }

    @GET
    @Path("/login")
    @Produces("application/json")
    public Response login(@QueryParam("user") String user, @QueryParam("pass") String pass){
        System.out.println("login info: " + user + " " + pass);
        SqlServer loginQuery = new SqlServer();
        return Response.ok(loginQuery.login(user, pass)).header("Access-Control-Allow-Origin", "*").build();
    }
}