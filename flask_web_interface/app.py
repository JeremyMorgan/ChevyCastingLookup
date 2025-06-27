from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from api_client import CastingAPIClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Initialize API client
api_client = CastingAPIClient()

@app.route('/')
def index():
    """Home page with search forms."""
    # Check API status
    api_status = api_client.health_check()
    return render_template('index.html', api_status=api_status)

@app.route('/search', methods=['POST'])
def search_casting():
    """Search for a specific casting number."""
    casting_number = request.form.get('casting_number', '').strip()
    
    if not casting_number:
        flash('Please enter a casting number.', 'error')
        return redirect(url_for('index'))
    
    try:
        casting = api_client.get_casting_by_id(casting_number)
        
        if casting:
            # Single result - redirect to detail page
            return redirect(url_for('casting_detail', casting_id=casting_number))
        else:
            flash(f'No casting found with number: {casting_number}', 'warning')
            return redirect(url_for('index'))
            
    except Exception as e:
        logger.error(f"Error searching for casting {casting_number}: {str(e)}")
        flash(f'Error searching for casting: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/advanced-search', methods=['GET', 'POST'])
def advanced_search():
    """Advanced search with multiple criteria."""
    if request.method == 'GET':
        # Handle GET requests with query parameters (from links)
        search_params = {
            'years': request.args.get('years', ''),
            'cid': request.args.get('cid', ''),
            'main_caps': request.args.get('main_caps', ''),
            'comments': request.args.get('comments', '')
        }
    else:
        # Handle POST requests from form
        search_params = {
            'years': request.form.get('years', '').strip(),
            'cid': request.form.get('cid', '').strip(),
            'main_caps': request.form.get('main_caps', '').strip(),
            'comments': request.form.get('comments', '').strip()
        }
    
    # Check if at least one search parameter is provided
    if not any(search_params.values()):
        flash('Please enter at least one search criteria.', 'warning')
        return redirect(url_for('index'))
    
    try:
        # Convert CID to int if provided
        cid = None
        if search_params['cid']:
            try:
                cid = int(search_params['cid'])
            except ValueError:
                flash('CID must be a number.', 'error')
                return redirect(url_for('index'))
        
        castings = api_client.search_castings(
            years=search_params['years'] or None,
            cid=cid,
            main_caps=search_params['main_caps'] or None,
            comments=search_params['comments'] or None
        )
        
        return render_template('results.html', 
                             castings=castings, 
                             search_params=search_params)
        
    except Exception as e:
        logger.error(f"Error in advanced search: {str(e)}")
        flash(f'Error performing search: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/browse')
def browse_all():
    """Browse all castings with pagination."""
    page = request.args.get('page', 1, type=int)
    per_page = 50
    skip = (page - 1) * per_page
    
    try:
        castings = api_client.get_all_castings(skip=skip, limit=per_page)
        
        # Simple pagination info
        has_next = len(castings) == per_page
        has_prev = page > 1
        
        return render_template('results.html', 
                             castings=castings,
                             page=page,
                             has_next=has_next,
                             has_prev=has_prev,
                             show_pagination=True)
        
    except Exception as e:
        logger.error(f"Error browsing castings: {str(e)}")
        flash(f'Error loading castings: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/casting/<casting_id>')
def casting_detail(casting_id):
    """Display detailed information for a specific casting."""
    try:
        casting = api_client.get_casting_by_id(casting_id)
        
        if not casting:
            flash(f'Casting {casting_id} not found.', 'error')
            return redirect(url_for('index'))
        
        return render_template('casting_detail.html', casting=casting)
        
    except Exception as e:
        logger.error(f"Error getting casting details for {casting_id}: {str(e)}")
        flash(f'Error loading casting details: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/health')
def api_health():
    """Check API health status."""
    try:
        status = api_client.health_check()
        return jsonify({
            'status': 'connected' if status else 'disconnected',
            'api_url': api_client.base_url
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
