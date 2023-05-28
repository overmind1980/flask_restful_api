from flask import Flask,request,jsonify
import json
from flask import Blueprint
from db import pool

module_task = Blueprint("task", __name__)

@module_task.route("/task/delete",methods=["DELETE"])
def task_delete():
    task_dict = request.get_json()
    print("task_dict==========",task_dict)
    task_id = task_dict.get("task_id")
    status_code = 200
    response_headers =  {"Content-Type": "application/json"}
    if not task_id:
        return "task_id is none", status_code, response_headers
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                sql = """DELETE FROM task WHERE id=%s"""
                t = (task_id, )
                print("sql=========",sql)
                cur.execute(sql,t)
                conn.commit()
                return "delete successful", status_code, response_headers
    except:
        return "delete failed!", status_code, response_headers

@module_task.route("/task/update",methods=["PUT"])
def task_update():
    task_dict = request.get_json()
    print("task_dict==========",task_dict)
    task_id = task_dict.get("task_id")
    task_name = task_dict.get("task_name")
    task_detail = task_dict.get("task_detail")
    status_code = 200
    response_headers =  {"Content-Type": "application/json"}
    if not task_name or not task_detail :
        return "task_name and task_detail cannot be none", status_code, response_headers
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                sql = """UPDATE task SET task_name=%s, task_detail=%s WHERE id=%s"""
                print(sql)
                t = (task_name, task_detail,task_id)
                print(t)
                cur.execute(sql,t)
                conn.commit()
                return "update successful", status_code, response_headers
    except:
        return "update failed!", status_code, response_headers

@module_task.route("/task/insert",methods=["POST"])
def task_insert():
    task_dict = request.get_json()
    print("task_dict==========",task_dict)
    task_name = task_dict.get("task_name")
    task_detail = task_dict.get("task_detail")
    status_code = 200
    response_headers =  {"Content-Type": "application/json"}
    if not task_name or not task_detail :
        return "task_name and task_detail cannot be none", status_code, response_headers
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                sql = """INSERT INTO task(task_name,task_detail) VALUES(%s,%s)"""
                t = (task_name, task_detail)
                cur.execute(sql,t)
                conn.commit()
                return "insert successful", status_code, response_headers
    except:
        return "insert failed!", status_code, response_headers

@module_task.route("/task/tasks",methods=["POST","GET"])
def get_all_tasks():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                sql = """SELECT id,task_name,task_detail FROM task ORDER BY id"""
                cur.execute(sql)
                records = cur.fetchall()
                l_tasks = []
                for record in records:
                    result = {}
                    result["id"] = record[0]
                    result["task_name"] = record[1]
                    result["task_detail"] = record[2]
                    l_tasks.append(result)
                str_tasks = str(l_tasks)
                print("str_tasks=========", str_tasks)
                return str(str_tasks)
    except:
        return "cannot get all tasks!"

@module_task.route("/task/search_tasks",methods=["POST","GET"])
def search_tasks():
    task_dict = request.get_json()
    print("task_dict==========",task_dict)
    task_name = task_dict.get("task_name")
    task_detail = task_dict.get("task_detail")
    if task_name == None :
        return "{\"msg\":\"task_name is None\"}"
    if task_detail == None:
        return "{\"msg\":\"task_detail is None\"}"
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                pattern1 = "%" + task_name + "%"
                pattern2 = "%" + task_detail + "%"
                sql = """SELECT id,task_name,task_detail FROM task WHERE task_name LIKE %s and task_detail LIKE %s ORDER BY id"""
                print(sql)
                t = (pattern1, pattern2)
                print(t)
                cur.execute(sql,t)
                records = cur.fetchall()
                l_tasks = []
                for record in records:
                    result = {}
                    result["id"] = record[0]
                    result["task_name"] = record[1]
                    result["task_detail"] = record[2]
                    l_tasks.append(result)
                str_tasks = str(l_tasks)
                print("str_tasks=========", str_tasks)
                return str(str_tasks)
    except:
        return "{\"msg\":\"cannot search tasks\"}"
