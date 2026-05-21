from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated

# pydantic model to validate incoming data
class UserInput(BaseModel):

    previous_score: Annotated[int, Field(..., gt=0, lt=100, description='Previous score of the student')]
    study_hours: Annotated[int, Field(..., gt=0, lt=24, description='Number of hours the student studies per day')]
    attendance: Annotated[int, Field(..., gt=0, lt=100, description='% Attendance of the student')]
    sleep_hours: Annotated[int, Field(..., gt=0, lt=24, description='Number of hours the student sleeps per day')]
    assignments_completed: Annotated[int, Field(..., ge=0, description='Number of assignments completed by the student')]
    internet_usage: Annotated[int, Field(..., gt=0, lt=24, description='Number of hours the student spends on internet per day')]
    exam_score: Annotated[float, Field(..., gt=0, lt=100, description='Exam score of the student')]
    
    # occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
    #    'business_owner', 'unemployed', 'private_job'], Field(..., description='Occupation of the student')]
    
    # =========================================================
    # Engineered Features
    # =========================================================

    @computed_field
    @property
    def study_efficiency(self) -> float:
        return self.previous_score / (self.study_hours + 1)

    @computed_field
    @property
    def engagement_score(self) -> float:
        return self.attendance * self.study_hours

    @computed_field
    @property
    def healthy_routine(self) -> float:
        return self.sleep_hours * self.attendance

    @computed_field
    @property
    def productivity_score(self) -> float:
        return (
            self.study_hours +
            self.assignments_completed +
            self.attendance / 10
        )

    @computed_field
    @property
    def internet_to_study_ratio(self) -> float:
        return self.internet_usage / (self.study_hours + 1)

    @computed_field
    @property
    def improvement_percent(self) -> float:
        return (
            (self.exam_score - self.previous_score) /
            (self.previous_score + 1)
        )

    @computed_field
    @property
    def attendance_category(self) -> str:
        if self.attendance <= 60:
            return "Low"
        elif self.attendance <= 80:
            return "Medium"
        return "High"

    @computed_field
    @property
    def sleep_category(self) -> str:
        if self.sleep_hours <= 5:
            return "Poor"
        elif self.sleep_hours <= 7:
            return "Average"
        return "Good"

    @computed_field
    @property
    def study_level(self) -> str:
        if self.study_hours <= 2:
            return "Low"
        elif self.study_hours <= 5:
            return "Medium"
        return "High"

    @computed_field
    @property
    def academic_strength(self) -> float:
        return (
            0.4 * self.previous_score +
            0.6 * self.exam_score
        )

    @computed_field
    @property
    def discipline_score(self) -> float:
        return (
            self.attendance +
            self.assignments_completed * 10 -
            self.internet_usage
        )
    