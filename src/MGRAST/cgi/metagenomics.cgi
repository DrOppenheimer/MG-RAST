use strict;
use warnings;
no warnings 'once';

use WebApplication;
use WebMenu;
use WebLayout;
use WebConfig;

use Conf;

eval {
    &main;
};

if ($@)
{
    my $cgi = new CGI();

    print $cgi->header();
    print $cgi->start_html();
    
    # print out the error
    print '<pre>'.$@.'</pre>';

    print $cgi->end_html();

}

sub main {
    my $range = 2;
    my $random_number = int(rand($range));

    my $layout = WebLayout->new($Conf::html_base.'/MGRAST.tmpl');
    $layout->add_template($Conf::html_base.'/EmptyLayout.tmpl', ["Home2"]);
    $layout->add_template($Conf::html_base.'/MGRAST-frontpage.tmpl', ["Home"]);
    $layout->add_css($Conf::cgi_url."/Html/mgrast.css");
    $layout->add_css($Conf::cgi_url."/Html/formalize.css");
    $layout->add_javascript($Conf::cgi_url."/Html/jquery.1.7.2.min.js");
    $layout->add_javascript($Conf::cgi_url."/Html/jquery.formalize.min.js");
    $layout->add_javascript($Conf::cgi_url."/Html/raphael-min.js");
    $layout->show_icon(1);
    $layout->icon_path($Conf::cgi_url."/Html/favicon.ico");

    # build menu
    my $menu = WebMenu->new();
    $menu->style('horizontal');

    # initialize application
    my $WebApp = WebApplication->new( { id       => 'MGRAST',
					menu     => $menu,
					layout   => $layout,
					default  => 'Home',
				      } );
    $WebApp->strict_browser(1);
    $WebApp->page_title_prefix('MG-RAST - ');
    $WebApp->show_login_user_info(1);
    $WebApp->fancy_login(1);

    # set metatags
    if ($WebApp->cgi->param('page') && $WebApp->cgi->param('page') ne 'Home') {
	$WebApp->metatags("robots", "nofollow");
    } else {
	$WebApp->metatags("robots", "index,follow");
    }
    $WebApp->metatags("description", "MG-RAST (the Metagenomics RAST) server is an automated analysis platform for metagenomes providing quantitative insights into microbial populations based on sequence data. The server primarily provides upload, quality control, automated annotation and analysis for prokaryotic metagenomic shotgun samples.");
    $WebApp->metatags("keywords", "metagenomics, MG-RAST, mgrast, prokaryotic, metagenome, shotgun, qc, quality control, upload, publish, 454, illumina, solexa, histogram, pca, pcoa, blast, blat, recruitment plot, environment, metadata, biodiversity, analysis, automation, api, search");

    # run application
    $WebApp->run();

}
