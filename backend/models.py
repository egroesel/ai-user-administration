from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    profile_slug = Column(String(255), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 2FA fields
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(32), nullable=True)

    # Password reset
    reset_token = Column(String(255), nullable=True)
    reset_token_expires = Column(DateTime(timezone=True), nullable=True)

    # Magic link login
    magic_link_token = Column(String(255), nullable=True)
    magic_link_expires = Column(DateTime(timezone=True), nullable=True)

    # Project starter role
    is_starter = Column(Boolean, default=False)

    # Relationship to projects
    projects = relationship("Project", back_populates="owner")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    short_description = Column(String(500), nullable=True)

    # Funding details
    funding_goal = Column(Numeric(12, 2), nullable=True)
    funding_current = Column(Numeric(12, 2), default=0)

    # Status: draft, submitted, verified, financing, ended_success, ended_failed
    status = Column(String(50), default="draft")

    # Project type: crowdfunding, fundraising, private
    project_type = Column(String(50), default="crowdfunding")

    # Dates
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    financing_start = Column(DateTime(timezone=True), nullable=True)
    financing_end = Column(DateTime(timezone=True), nullable=True)

    # Media
    image_url = Column(String(500), nullable=True)
    video_url = Column(String(500), nullable=True)

    # Relationship
    owner = relationship("User", back_populates="projects")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    session_token = Column(String(255), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
