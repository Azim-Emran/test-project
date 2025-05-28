from flask import jsonify, Blueprint
from models.models import QuizResult
from models.models import db

assistant_api_bp = Blueprint('assistant_api', __name__)

@assistant_api_bp.route('/admin/performance', methods=['GET'])
def admin_performance():
    from models.models import QuizResult
    from sqlalchemy import func
    results = (
        db.session.query(
            QuizResult.user_id.label('student_id'),
            QuizResult.topic,
            func.avg(QuizResult.is_correct.cast(db.Float)).label('accuracy'),
            func.count().label('total')
        )
        .group_by(QuizResult.user_id, QuizResult.topic)
        .all()
    )
    return jsonify([
        {
            'student_id': r.student_id,
            'topic': r.topic,
            'accuracy': r.accuracy * 100,
            'total': r.total
        } for r in results
    ])
