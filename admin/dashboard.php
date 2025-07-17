<?php
session_start();

// Check authentication
if (!isset($_SESSION['admin_logged_in']) || !$_SESSION['admin_logged_in']) {
    header('Location: /admin/');
    exit;
}

// Handle different sections
$section = $_GET['section'] ?? 'dashboard';
$action = $_GET['action'] ?? '';

// Handle form submissions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if ($action === 'save_site_settings') {
        // Save site settings
        $settings = [
            'site_name' => $_POST['site_name'] ?? '',
            'site_description' => $_POST['site_description'] ?? '',
            'site_url' => $_POST['site_url'] ?? '',
            'admin_email' => $_POST['admin_email'] ?? '',
            'seo_title' => $_POST['seo_title'] ?? '',
            'seo_description' => $_POST['seo_description'] ?? '',
            'analytics_code' => $_POST['analytics_code'] ?? '',
        ];
        
        // Save to JSON file (in production, use a database)
        file_put_contents('data/site_settings.json', json_encode($settings, JSON_PRETTY_PRINT));
        $success_message = 'Site settings saved successfully!';
    }
    
    if ($action === 'save_review') {
        // Save review
        $review = [
            'id' => $_POST['id'] ?? uniqid(),
            'name' => $_POST['name'] ?? '',
            'rating' => $_POST['rating'] ?? 0,
            'bonus' => $_POST['bonus'] ?? '',
            'description' => $_POST['description'] ?? '',
            'features' => array_filter(explode(',', $_POST['features'] ?? '')),
            'pros' => array_filter(explode(',', $_POST['pros'] ?? '')),
            'cons' => array_filter(explode(',', $_POST['cons'] ?? '')),
            'referral_link' => $_POST['referral_link'] ?? '',
            'logo' => $_POST['logo'] ?? '',
            'status' => $_POST['status'] ?? 'active',
            'created_at' => date('Y-m-d H:i:s'),
            'updated_at' => date('Y-m-d H:i:s')
        ];
        
        // Load existing reviews
        $reviews = [];
        if (file_exists('data/reviews.json')) {
            $reviews = json_decode(file_get_contents('data/reviews.json'), true) ?? [];
        }
        
        // Add or update review
        $found = false;
        foreach ($reviews as $key => $existingReview) {
            if ($existingReview['id'] === $review['id']) {
                $reviews[$key] = $review;
                $found = true;
                break;
            }
        }
        
        if (!$found) {
            $reviews[] = $review;
        }
        
        // Save reviews
        if (!file_exists('data')) {
            mkdir('data', 0755, true);
        }
        file_put_contents('data/reviews.json', json_encode($reviews, JSON_PRETTY_PRINT));
        $success_message = 'Review saved successfully!';
    }
}

// Load data
$site_settings = [];
if (file_exists('data/site_settings.json')) {
    $site_settings = json_decode(file_get_contents('data/site_settings.json'), true) ?? [];
}

$reviews = [];
if (file_exists('data/reviews.json')) {
    $reviews = json_decode(file_get_contents('data/reviews.json'), true) ?? [];
}

// Get specific review for editing
$current_review = null;
if ($section === 'reviews' && $action === 'edit' && isset($_GET['id'])) {
    $review_id = $_GET['id'];
    foreach ($reviews as $review) {
        if ($review['id'] === $review_id) {
            $current_review = $review;
            break;
        }
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - GamblingReviews</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            color: #333;
        }
        
        .admin-container {
            display: flex;
            min-height: 100vh;
        }
        
        .sidebar {
            width: 250px;
            background: #2c3e50;
            color: white;
            padding: 1rem 0;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
        }
        
        .sidebar-header {
            padding: 0 1rem 2rem;
            border-bottom: 1px solid #34495e;
        }
        
        .sidebar-header h2 {
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
        }
        
        .sidebar-header p {
            font-size: 0.9rem;
            opacity: 0.8;
        }
        
        .sidebar-nav {
            list-style: none;
            padding: 1rem 0;
        }
        
        .sidebar-nav li {
            margin-bottom: 0.5rem;
        }
        
        .sidebar-nav a {
            display: flex;
            align-items: center;
            padding: 0.75rem 1rem;
            color: white;
            text-decoration: none;
            transition: background 0.3s;
        }
        
        .sidebar-nav a:hover,
        .sidebar-nav a.active {
            background: #3498db;
        }
        
        .sidebar-nav i {
            margin-right: 0.75rem;
            width: 20px;
        }
        
        .main-content {
            flex: 1;
            margin-left: 250px;
            padding: 2rem;
        }
        
        .top-bar {
            background: white;
            padding: 1rem 2rem;
            margin: -2rem -2rem 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .top-bar h1 {
            font-size: 1.5rem;
            color: #2c3e50;
        }
        
        .user-menu {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .user-menu a {
            color: #2c3e50;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            transition: background 0.3s;
        }
        
        .user-menu a:hover {
            background: #f8f9fa;
        }
        
        .card {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .card h3 {
            margin-bottom: 1rem;
            color: #2c3e50;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-card h4 {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        .stat-card p {
            opacity: 0.9;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        .form-group input,
        .form-group textarea,
        .form-group select {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 1rem;
        }
        
        .form-group textarea {
            min-height: 120px;
            resize: vertical;
        }
        
        .btn {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            background: #3498db;
            color: white;
            text-decoration: none;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 1rem;
            transition: background 0.3s;
        }
        
        .btn:hover {
            background: #2980b9;
        }
        
        .btn-success {
            background: #27ae60;
        }
        
        .btn-success:hover {
            background: #219a52;
        }
        
        .btn-danger {
            background: #e74c3c;
        }
        
        .btn-danger:hover {
            background: #c0392b;
        }
        
        .btn-small {
            padding: 0.5rem 1rem;
            font-size: 0.9rem;
        }
        
        .table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }
        
        .table th,
        .table td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        .table th {
            background: #f8f9fa;
            font-weight: 500;
        }
        
        .table tr:hover {
            background: #f8f9fa;
        }
        
        .success {
            background: #d4edda;
            color: #155724;
            padding: 1rem;
            border-radius: 4px;
            border: 1px solid #c3e6cb;
            margin-bottom: 1rem;
        }
        
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 1rem;
            border-radius: 4px;
            border: 1px solid #f5c6cb;
            margin-bottom: 1rem;
        }
        
        .rating-input {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .rating-input input {
            width: 80px;
        }
        
        .feature-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }
        
        .feature-tag {
            background: #e9ecef;
            padding: 0.25rem 0.5rem;
            border-radius: 12px;
            font-size: 0.8rem;
        }
        
        @media (max-width: 768px) {
            .sidebar {
                width: 200px;
            }
            
            .main-content {
                margin-left: 200px;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="admin-container">
        <aside class="sidebar">
            <div class="sidebar-header">
                <h2>GamblingReviews</h2>
                <p>Admin Panel</p>
            </div>
            
            <nav>
                <ul class="sidebar-nav">
                    <li><a href="?section=dashboard" class="<?php echo $section === 'dashboard' ? 'active' : ''; ?>">
                        <i class="fas fa-tachometer-alt"></i> Dashboard
                    </a></li>
                    <li><a href="?section=reviews" class="<?php echo $section === 'reviews' ? 'active' : ''; ?>">
                        <i class="fas fa-star"></i> Reviews
                    </a></li>
                    <li><a href="?section=sites" class="<?php echo $section === 'sites' ? 'active' : ''; ?>">
                        <i class="fas fa-globe"></i> Gambling Sites
                    </a></li>
                    <li><a href="?section=analytics" class="<?php echo $section === 'analytics' ? 'active' : ''; ?>">
                        <i class="fas fa-chart-line"></i> Analytics
                    </a></li>
                    <li><a href="?section=settings" class="<?php echo $section === 'settings' ? 'active' : ''; ?>">
                        <i class="fas fa-cog"></i> Settings
                    </a></li>
                    <li><a href="?section=seo" class="<?php echo $section === 'seo' ? 'active' : ''; ?>">
                        <i class="fas fa-search"></i> SEO
                    </a></li>
                </ul>
            </nav>
        </aside>
        
        <main class="main-content">
            <div class="top-bar">
                <h1>
                    <?php
                    $titles = [
                        'dashboard' => 'Dashboard',
                        'reviews' => 'Reviews Management',
                        'sites' => 'Gambling Sites',
                        'analytics' => 'Analytics',
                        'settings' => 'Site Settings',
                        'seo' => 'SEO Management'
                    ];
                    echo $titles[$section] ?? 'Admin Panel';
                    ?>
                </h1>
                <div class="user-menu">
                    <span>Welcome, <?php echo $_SESSION['admin_username']; ?></span>
                    <a href="/" target="_blank"><i class="fas fa-external-link-alt"></i> View Site</a>
                    <a href="?logout=1"><i class="fas fa-sign-out-alt"></i> Logout</a>
                </div>
            </div>
            
            <?php if (isset($success_message)): ?>
                <div class="success"><?php echo htmlspecialchars($success_message); ?></div>
            <?php endif; ?>
            
            <?php if ($section === 'dashboard'): ?>
                <div class="stats-grid">
                    <div class="stat-card">
                        <h4><?php echo count($reviews); ?></h4>
                        <p>Total Reviews</p>
                    </div>
                    <div class="stat-card">
                        <h4><?php echo count(array_filter($reviews, function($r) { return $r['status'] === 'active'; })); ?></h4>
                        <p>Active Reviews</p>
                    </div>
                    <div class="stat-card">
                        <h4>0</h4>
                        <p>Total Visitors</p>
                    </div>
                    <div class="stat-card">
                        <h4>0</h4>
                        <p>Referral Clicks</p>
                    </div>
                </div>
                
                <div class="card">
                    <h3>Recent Activity</h3>
                    <p>No recent activity to display.</p>
                </div>
                
                <div class="card">
                    <h3>Quick Actions</h3>
                    <div style="display: flex; gap: 1rem;">
                        <a href="?section=reviews&action=new" class="btn">Add New Review</a>
                        <a href="?section=settings" class="btn">Site Settings</a>
                        <a href="?section=analytics" class="btn">View Analytics</a>
                    </div>
                </div>
            
            <?php elseif ($section === 'reviews'): ?>
                <?php if ($action === 'new' || $action === 'edit'): ?>
                    <div class="card">
                        <h3><?php echo $action === 'new' ? 'Add New Review' : 'Edit Review'; ?></h3>
                        <form method="POST" action="?section=reviews&action=save_review">
                            <?php if ($current_review): ?>
                                <input type="hidden" name="id" value="<?php echo htmlspecialchars($current_review['id']); ?>">
                            <?php endif; ?>
                            
                            <div class="form-group">
                                <label for="name">Site Name</label>
                                <input type="text" id="name" name="name" value="<?php echo htmlspecialchars($current_review['name'] ?? ''); ?>" required>
                            </div>
                            
                            <div class="form-group">
                                <label for="rating">Rating (1-100)</label>
                                <div class="rating-input">
                                    <input type="number" id="rating" name="rating" min="1" max="100" value="<?php echo htmlspecialchars($current_review['rating'] ?? ''); ?>" required>
                                    <span>%</span>
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label for="bonus">Welcome Bonus</label>
                                <input type="text" id="bonus" name="bonus" value="<?php echo htmlspecialchars($current_review['bonus'] ?? ''); ?>" placeholder="e.g., 125% up to $3,750">
                            </div>
                            
                            <div class="form-group">
                                <label for="description">Description</label>
                                <textarea id="description" name="description" placeholder="Enter site description..."><?php echo htmlspecialchars($current_review['description'] ?? ''); ?></textarea>
                            </div>
                            
                            <div class="form-group">
                                <label for="features">Features (comma-separated)</label>
                                <input type="text" id="features" name="features" value="<?php echo htmlspecialchars(implode(', ', $current_review['features'] ?? [])); ?>" placeholder="e.g., 500+ Games, Fast Payouts, 24/7 Support">
                            </div>
                            
                            <div class="form-group">
                                <label for="pros">Pros (comma-separated)</label>
                                <input type="text" id="pros" name="pros" value="<?php echo htmlspecialchars(implode(', ', $current_review['pros'] ?? [])); ?>" placeholder="e.g., Great game selection, Quick withdrawals">
                            </div>
                            
                            <div class="form-group">
                                <label for="cons">Cons (comma-separated)</label>
                                <input type="text" id="cons" name="cons" value="<?php echo htmlspecialchars(implode(', ', $current_review['cons'] ?? [])); ?>" placeholder="e.g., Limited customer support hours">
                            </div>
                            
                            <div class="form-group">
                                <label for="referral_link">Referral Link</label>
                                <input type="url" id="referral_link" name="referral_link" value="<?php echo htmlspecialchars($current_review['referral_link'] ?? ''); ?>" placeholder="https://...">
                            </div>
                            
                            <div class="form-group">
                                <label for="logo">Logo URL</label>
                                <input type="url" id="logo" name="logo" value="<?php echo htmlspecialchars($current_review['logo'] ?? ''); ?>" placeholder="https://...">
                            </div>
                            
                            <div class="form-group">
                                <label for="status">Status</label>
                                <select id="status" name="status">
                                    <option value="active" <?php echo ($current_review['status'] ?? '') === 'active' ? 'selected' : ''; ?>>Active</option>
                                    <option value="inactive" <?php echo ($current_review['status'] ?? '') === 'inactive' ? 'selected' : ''; ?>>Inactive</option>
                                    <option value="draft" <?php echo ($current_review['status'] ?? '') === 'draft' ? 'selected' : ''; ?>>Draft</option>
                                </select>
                            </div>
                            
                            <div style="display: flex; gap: 1rem;">
                                <button type="submit" class="btn btn-success">Save Review</button>
                                <a href="?section=reviews" class="btn">Cancel</a>
                            </div>
                        </form>
                    </div>
                <?php else: ?>
                    <div class="card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                            <h3>All Reviews</h3>
                            <a href="?section=reviews&action=new" class="btn">Add New Review</a>
                        </div>
                        
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Rating</th>
                                    <th>Bonus</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($reviews as $review): ?>
                                    <tr>
                                        <td><?php echo htmlspecialchars($review['name']); ?></td>
                                        <td><?php echo htmlspecialchars($review['rating']); ?>%</td>
                                        <td><?php echo htmlspecialchars($review['bonus']); ?></td>
                                        <td>
                                            <span class="feature-tag"><?php echo htmlspecialchars($review['status']); ?></span>
                                        </td>
                                        <td>
                                            <a href="?section=reviews&action=edit&id=<?php echo htmlspecialchars($review['id']); ?>" class="btn btn-small">Edit</a>
                                            <a href="?section=reviews&action=delete&id=<?php echo htmlspecialchars($review['id']); ?>" class="btn btn-small btn-danger" onclick="return confirm('Are you sure?')">Delete</a>
                                        </td>
                                    </tr>
                                <?php endforeach; ?>
                                
                                <?php if (empty($reviews)): ?>
                                    <tr>
                                        <td colspan="5" style="text-align: center; color: #666;">No reviews found. <a href="?section=reviews&action=new">Add your first review</a></td>
                                    </tr>
                                <?php endif; ?>
                            </tbody>
                        </table>
                    </div>
                <?php endif; ?>
            
            <?php elseif ($section === 'settings'): ?>
                <div class="card">
                    <h3>Site Settings</h3>
                    <form method="POST" action="?section=settings&action=save_site_settings">
                        <div class="form-group">
                            <label for="site_name">Site Name</label>
                            <input type="text" id="site_name" name="site_name" value="<?php echo htmlspecialchars($site_settings['site_name'] ?? 'GamblingReviews'); ?>">
                        </div>
                        
                        <div class="form-group">
                            <label for="site_description">Site Description</label>
                            <textarea id="site_description" name="site_description"><?php echo htmlspecialchars($site_settings['site_description'] ?? ''); ?></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="site_url">Site URL</label>
                            <input type="url" id="site_url" name="site_url" value="<?php echo htmlspecialchars($site_settings['site_url'] ?? ''); ?>">
                        </div>
                        
                        <div class="form-group">
                            <label for="admin_email">Admin Email</label>
                            <input type="email" id="admin_email" name="admin_email" value="<?php echo htmlspecialchars($site_settings['admin_email'] ?? ''); ?>">
                        </div>
                        
                        <div class="form-group">
                            <label for="seo_title">SEO Title</label>
                            <input type="text" id="seo_title" name="seo_title" value="<?php echo htmlspecialchars($site_settings['seo_title'] ?? ''); ?>">
                        </div>
                        
                        <div class="form-group">
                            <label for="seo_description">SEO Description</label>
                            <textarea id="seo_description" name="seo_description"><?php echo htmlspecialchars($site_settings['seo_description'] ?? ''); ?></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="analytics_code">Analytics Code (Google Analytics)</label>
                            <textarea id="analytics_code" name="analytics_code" placeholder="Paste your Google Analytics code here..."><?php echo htmlspecialchars($site_settings['analytics_code'] ?? ''); ?></textarea>
                        </div>
                        
                        <button type="submit" class="btn btn-success">Save Settings</button>
                    </form>
                </div>
            
            <?php elseif ($section === 'analytics'): ?>
                <div class="card">
                    <h3>Analytics Overview</h3>
                    <p>Analytics integration coming soon. This will include:</p>
                    <ul style="margin-top: 1rem;">
                        <li>Referral click tracking</li>
                        <li>Conversion rates</li>
                        <li>User behavior analysis</li>
                        <li>Revenue tracking</li>
                    </ul>
                </div>
            
            <?php elseif ($section === 'seo'): ?>
                <div class="card">
                    <h3>SEO Management</h3>
                    <p>SEO tools and optimization features coming soon. This will include:</p>
                    <ul style="margin-top: 1rem;">
                        <li>Meta tags management</li>
                        <li>Sitemap generation</li>
                        <li>Schema markup</li>
                        <li>Page speed optimization</li>
                    </ul>
                </div>
            
            <?php else: ?>
                <div class="card">
                    <h3>Page Not Found</h3>
                    <p>The requested page could not be found.</p>
                </div>
            <?php endif; ?>
        </main>
    </div>
</body>
</html>