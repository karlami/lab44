package com.api.connection;

import com.microsoft.sqlserver.jdbc.SQLServerDriver;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class SqlServer {

    private static final String database = "proyect2_database";
    private static final String password = "ProyectSOA123";
    private static final String port = "1433";

    private Connection base_init_conn() {
        try {
            DriverManager.registerDriver(new SQLServerDriver());
            String dbURL = "jdbc:sqlserver://192.168.32.2:" + port + ";databaseName=" + database + ";user=sa;password="+ password;
            Connection conn = DriverManager.getConnection(dbURL);
            if (conn != null) {
                System.out.println("Connected to SQL Server database");
                return conn;
            }else{
                System.out.println("Couldn't connect to SQL Server database");
            }
        } catch (SQLException throwables) {
            throwables.printStackTrace();
        }
        return null;
    }

    public List<String> getNames(){
        Connection conn = base_init_conn();
        String selectSql = "SELECT firstName FROM Person";
        PreparedStatement pstm = null;
        List<String> names = new ArrayList<String>();
        try {
            assert conn != null;
            pstm = conn.prepareStatement(selectSql);
            ResultSet rs = pstm.executeQuery();
            while (rs.next()){
                names.add(rs.getString(1));
            }
            return names;
        } catch (SQLException throwables) {
            throwables.printStackTrace();
        }
        return names;
    }

    public String login(String user, String pass){
        String res = "{\"status\": \"not found\"}";
        Connection conn = base_init_conn();
        //String selectSql = "SELECT * FROM Account WHERE userName = ? AND securityKey = ?;";
        String selectSql = "DECLARE  @return_status bit  \n" +
                " EXEC @return_status= securityLogin @userName = ?, @securityKey = ? \n" +
                " SELECT @return_status AS securityLogin;";
        PreparedStatement pstm = null;
        try {
            assert conn != null;
            pstm = conn.prepareStatement(selectSql);
            pstm.setString(1, user);
            pstm.setString(2, pass);
            ResultSet rs = pstm.executeQuery();
            rs.next();
            if (rs.getString(1).equals("1")){
                res = "{\"status\": \"ok\"}";
            }
        } catch (SQLException throwables) {
            throwables.printStackTrace();
        }
        return res;
    }
}


