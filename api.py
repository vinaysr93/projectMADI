from flask_restful import Resource,fields,marshal_with
from database import db

from validation import NotFoundError,InternalServerError
output_fields={
        "course_id":fields.Integer,
        "course_name":fields.String,
        "course_code":fields.String,
        "course_description":fields.String

}


class CourseAPI(Resource):

    @marshal_with(output_fields)
    def get(self,course_id):

        print("GET course_id",course_id)
        try:
            query=Course.query.filter_by(course_id=course_id).first()

        except:

            raise InternalServerError(status_code=500)
        if query:
            # qcourse_id=query.course_id
            # qcourse_name=query.course_name
            # qcourse_code=query.course_code
            # qcourse_description=query.course_description

            return query

        else:

            raise NotFoundError(status_code=404)

    def put(self,course_id):
        print("PUT course_id",course_id)
        return {"course_id":course_id,"action":"PUT"}

    def delete(self,course_id):
        print("DELETE course_id", course_id)
        return {"course_id": course_id,"action":"DELETE"}

    def post(self,course_id):
        print("POST ")
        return {"action":"POST"}