import web
import models.project
from views.utils import get_nav_bar

# Get html templates
render = web.template.render('templates/')

class Index:
    
    def GET(self):
        """    
        Get main page using the projects URL input variable to
        determine which projects to show.
        
            :return: index page
        """

        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input(projects=None)

        if data:
            #Don't store project information in header. Avoid authorization bypass by clicking back arrow.
            web.header("Cache-Control", "no-cache, max-age=0, must-revalidate, no-store")           

        categories = models.project.get_categories()

        try:
            us = session.userid
            project_bulk_one = []
            project_bulk_two = []
            if data.projects == 'my':
                project_bulk_one = models.project.get_projects_by_status_and_owner(str(session.userid), "open")
                project_bulk_two = models.project.get_projects_by_status_and_owner(str(session.userid), "in progress")
            elif data.projects == 'customer':
                # TODO: Can customer projects be open?
                project_bulk_one = models.project.get_projects_by_participant_and_status(str(session.userid), "open")
                project_bulk_two = models.project.get_projects_by_participant_and_status(str(session.userid), "in progress")
            elif data.projects == 'finished':
                project_bulk_one = models.project.get_projects_by_status_and_owner(str(session.userid), "finished")
                project_bulk_two = models.project.get_projects_by_participant_and_status(str(session.userid), "finished")
        except:
            project_bulk_one = None
            project_bulk_two = None
        
        return render.index(nav, project_bulk_one, project_bulk_two, data.projects, categories)
