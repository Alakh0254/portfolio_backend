from pydantic import BaseModel
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class AdminUserBase(BaseModel):
    username: str

class AdminUserCreate(AdminUserBase):
    password: str

class PersonalProfileBase(BaseModel):
    name: str
    title: str
    tagline: str
    email: str
    phone: str
    location: str
    date_of_birth: Optional[str] = None
    fathers_name: Optional[str] = None
    nationality: Optional[str] = None
    profile_image_url: Optional[str] = None

class PersonalProfileCreate(PersonalProfileBase):
    pass

class PersonalProfileResponse(PersonalProfileBase):
    id: int
    class Config:
        from_attributes = True

class AboutSectionBase(BaseModel):
    title: str = "About Me"
    description: str
    image_url: Optional[str] = None
    resume_url: Optional[str] = None
    email: Optional[str] = None
    location: Optional[str] = None

class AboutSectionCreate(AboutSectionBase):
    pass

class AboutSectionResponse(AboutSectionBase):
    id: int
    class Config:
        from_attributes = True

class SocialLinkBase(BaseModel):
    platform: str
    url: str
    icon_class: Optional[str] = None

class SocialLinkCreate(SocialLinkBase):
    pass

class SocialLinkResponse(SocialLinkBase):
    id: int
    class Config:
        from_attributes = True

class SkillBase(BaseModel):
    category: str
    name: str
    proficiency: Optional[int] = None
    icon_class: Optional[str] = None
    icon_url: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillResponse(SkillBase):
    id: int
    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    title: str
    description: str
    image_url: str
    tags: str
    live_link: Optional[str] = None
    github_link: Optional[str] = None
    featured: bool = False

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    class Config:
        from_attributes = True

class ExperienceBase(BaseModel):
    role: str
    company: str
    duration: str
    description: str

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceResponse(ExperienceBase):
    id: int
    class Config:
        from_attributes = True

class EducationBase(BaseModel):
    degree: str
    institution: str
    duration: str
    description: str

class EducationCreate(EducationBase):
    pass

class EducationResponse(EducationBase):
    id: int
    class Config:
        from_attributes = True

class AchievementBase(BaseModel):
    title: str
    issuer: str
    date: str
    description: str

class AchievementCreate(AchievementBase):
    pass

class AchievementResponse(AchievementBase):
    id: int
    class Config:
        from_attributes = True
