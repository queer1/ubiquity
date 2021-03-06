import os

from autopilot.testcase import AutopilotTestCase
from autopilot.introspection import get_proxy_object_for_existing_process
from testtools.matchers import Equals, Contains
from autopilot.matchers import Eventually
from autopilot.input import Mouse, Pointer


class LvmEncryptInstallTests(AutopilotTestCase):
    
    def setUp(self):
        super(LvmEncryptInstallTests, self).setUp()
        self.app = self.launch_application()
        
        self.pointing_device = Pointer(Mouse.create())
        
    def launch_application(self):
        my_process = int(os.environ['UBIQUITY_PID'])
        my_dbus = str(os.environ['DBUS_SESSION_BUS_ADDRESS'])
        return get_proxy_object_for_existing_process(
            pid=my_process, dbus_bus=my_dbus)
    
    def test_lvm_encrypt_install(self):
        '''
            Test install using LVM and encryption configuration
        '''
        self.keyboard.press_and_release('Super+1')
        
        main_window = self.app.select_single(
            'GtkWindow', name='live_installer')
        self.assertThat(main_window.title, Equals("Install"))
        # This method runs the ubiquity_ methods to navigate
        # testing through the install pages
        self.run_lvm_encrypt_install_test()
        
        #Then finally here check that the complete dialog appears
        
        self.ubiquity_did_install_complete()
    
    def run_lvm_encrypt_install_test(self):
        '''
            this can be easily used when debugging. If the test exits on a
            particular page, you can comment out the pages prior to the exit point
            and reset current page to its default state, then run test again.
            The test will start from the page it exited on. This can save alot of
            hassle having to setup the whole test again, just to fix a small error.
        '''
        #Page 1
        self.ubiquity_welcome_page_test()
        #Page 2
        self.ubiquity_preparing_page_test()
        ##Page 3
        self.ubiquity_install_type_page_test()
        ##Page 3 extended
        self.ubiquity_lvm_password_encryption_page()
        #Page 4
        self.ubiquity_where_are_you_page_test()
        #Page 5
        self.ubiquity_keyboard_page_test()
        #Page 6
        self.ubiquity_who_are_you_page_test()
        #page 7
        self.ubiquity_progress_bar_test()
        
    def ubiquity_welcome_page_test(self):
        '''
            Tests that all needed objects on the Welcome page are accessible    
            And can also be navigated to.            
            Once confirmed continue with install accepting all defaults
        '''
        self.get_ubiquity_objects()
        
        self.assertThat(self.headerlabel.label, Eventually(Contains('Welcome')))
        #Can we navigate to the quit button? This fails the test if object
        # has no position attribs
        self.pointing_device.move_to_object(self.quit_button)
        self.assertThat(self.continue_button.label, Equals('Continue'))
        #Can we navigate to the continue button?
        self.pointing_device.move_to_object(self.continue_button)
        #Finally lets move on to the next page
        self.pointing_device.click()
        
    def ubiquity_preparing_page_test(self):
        
        self.wait_for_button_state_changed()
        #Check the next page title
        self.assertThat(self.headerlabel.label,
                        Eventually(Contains('Preparing to install')))
        #lets get all the page objects
        
        self.get_ubiquity_objects()
        '''
            Lets test we can go back to the welcome page and come back here
        '''
        #Click back
        self.pointing_device.move_to_object(self.back_button)
        self.pointing_device.click()
        
        self.wait_for_button_state_changed()
        #check we went back
        self.assertThat(self.headerlabel.label, Eventually(Contains('Welcome')))
        #go back to the page we were on
        self.get_ubiquity_objects()
        
        self.assertThat(self.continue_button.label, Equals('Continue'))
        self.pointing_device.move_to_object(self.continue_button)
        self.pointing_device.click()
        
        self.wait_for_button_state_changed()
        
        self.assertThat(self.headerlabel.label,
                        Eventually(Contains('Preparing to install')))
        
        '''
            Lets navigate round all objects
        '''
        # first need to get all objects again
        self.get_ubiquity_objects()
        #navigate to each one
        self.pointing_device.move_to_object(self.install_updates)
        self.pointing_device.move_to_object(self.third_party)
        self.pointing_device.move_to_object(self.back_button)
        self.pointing_device.move_to_object(self.quit_button)
        self.assertThat(self.continue_button.label, Equals('Continue'))
        self.pointing_device.move_to_object(self.continue_button)
        
        #Lets move on to next page now
        self.pointing_device.click()
        

    def ubiquity_install_type_page_test(self):

        """
            Check next page value
        """
        self.assertThat(self.headerlabel.label,
                        Eventually(Contains('Installation type')))
        #get all page objects
        self.get_ubiquity_objects()  
        '''
            Test we can go back to previous page and come back here
        '''
        #Go back
        self.pointing_device.move_to_object(self.back_button)
        self.pointing_device.click()

        self.wait_for_button_state_changed()

        self.assertThat(self.headerlabel.label,
                        Eventually(Contains('Preparing to install')))
        
        #To Come back again we need to get the objects of the preparing page
        self.get_ubiquity_objects()
        self.assertThat(self.continue_button.label, Equals('Continue'))
        self.pointing_device.move_to_object(self.continue_button)
        self.pointing_device.click()
        
        #check we came back ok
        self.assertThat(self.headerlabel.label,
                        Eventually(Contains('Installation type')))
        
        '''
            Lets check we can get and navigate to all the objects
            
            If we wanted to change the install type we can just add
            required clicks here for different installation types
        '''
        #Get all the page objects again
        self.get_ubiquity_objects()
        self.assertThat(self.erase_disk.label,
                        Contains('Erase disk and install'))
        self.pointing_device.move_to_object(self.erase_disk)
        self.pointing_device.move_to_object(self.lvm_install)
        self.pointing_device.move_to_object(self.something_else_install)
        self.pointing_device.move_to_object(self.encrypt_install)
        self.pointing_device.move_to_object(self.back_button)
        self.pointing_device.move_to_object(self.quit_button)
        self.pointing_device.move_to_object(self.continue_button)
        
        self.pointing_device.move_to_object(self.encrypt_install)
        self.pointing_device.click()
        #and now continue
        self.assertThat(self.continue_button.label, Equals('_Install Now'))
        self.pointing_device.move_to_object(self.continue_button)
        self.pointing_device.click()
        
    def ubiquity_lvm_password_encryption_page(self):
        self.get_ubiquity_objects()
        
        self.assertThat(self.headerlabel.label, Eventually(Contains('Choose a')))
        self.assertThat(self.password_grid.sensitive, Eventually(Equals(1)))
        
        self.pointing_device.move_to_object(self.encrypt_password)
        self.pointing_device.click()
        self.keyboard.type('EncryptedPassword')
        
        self.pointing_device.move_to_object(self.back_button)
        self.pointing_device.move_to_object(self.verify_encrypt_password)
        self.pointing_device.click()
        
        self.keyboard.type('EncryptedPassword')
        
        self.check_encrypted_passwords_match()
        #and continue
        self.pointing_device.move_to_object(self.continue_button)
        self.pointing_device.click()
        
    def check_encrypted_passwords_match(self):
        '''
        If passwords do not match then keep re-typing them till they match
        '''
        while True:

            self.continue_button = self.app.select_single('GtkButton',
                                                          name='next')
            button_sensitive = self.continue_button.sensitive

            if button_sensitive == 1:
                self.assertThat(self.continue_button.sensitive, Equals(1))
                break
            
            self.pointing_device.move_to_object(self.encrypt_password)
            self.pointing_device.click()
            self.keyboard.press_and_release('Ctrl+a')
            self.keyboard.type('EncryptedPassword')
        
            self.pointing_device.move_to_object(self.back_button)
            self.pointing_device.move_to_object(self.verify_encrypt_password)
            self.pointing_device.click()
            self.keyboard.press_and_release('Ctrl+a')
            self.keyboard.type('EncryptedPassword')
            
    def ubiquity_where_are_you_page_test(self):
        """
            From this point on the installation has started

            If you need to re-run the test from here then the HDD partitions
            need to be wiped
            and ./run_ubiquity run again
        """
        
        #check button activated
        self.wait_for_button_state_changed()
        self.get_ubiquity_objects()
        #check we are on the correct page. 
        self.assertThat(self.headerlabel.label,
                        Eventually(Contains('Where are you?')))
        
        #Not much to test on this page lets move on
        
        self.pointing_device.move_to_object(self.continue_button)
        
        self.pointing_device.click()
    
    def ubiquity_keyboard_page_test(self):
        #Check we are on the right page
        self.assertThat(self.headerlabel.label,
                        Eventually(Contains('Keyboard layout')))
        
        #get all the page objects
        self.get_ubiquity_objects()
        '''
            Test we can go back
        '''
        self.pointing_device.move_to_object(self.back_button)
        self.pointing_device.click()
        self.wait_for_button_state_changed()
        #check we went back ok
        self.assertThat(self.headerlabel.label,
                        Eventually(Contains('Where are you?')))
        
        #now lets go back
        
        self.continue_button = self.app.select_single('GtkButton',
                                                      name='next')
        self.pointing_device.move_to_object(self.continue_button)
        self.pointing_device.click()
        #wait for button to become active again
        self.wait_for_button_state_changed()
        #check we came back ok
        self.assertThat(self.headerlabel.label,
                        Eventually(Contains('Keyboard layout')))
        
        #We need to get the page objects again as the id's have changed
        self.get_ubiquity_objects()
        '''
            Test we can test keyboard
        '''
        self.pointing_device.move_to_object(self.keyboard_entry)
        self.pointing_device.click()
        self.keyboard.type('This is testing that we can enter text in this GtkEntry')
        '''
            Test we can navigate round the objects
        '''
        self.pointing_device.move_to_object(self.keyboard_layout)
        self.pointing_device.move_to_object(self.keyboard_entry)
        self.pointing_device.move_to_object(self.back_button)
        self.pointing_device.move_to_object(self.continue_button)
        #Lets move on to next page
        self.pointing_device.click()
    
    def ubiquity_who_are_you_page_test(self):
        """
            This method enters the new users details on the

            'Who are you?' page
        """
        #assert page title
        self.assertThat(self.headerlabel.label,
                        Eventually(Contains('Who are you')))
        self.get_ubiquity_objects()
        '''
            Test we can create a user
        '''
        self.keyboard.type('autopilot rocks')
        # Lets lose these tabs
        self.pointing_device.move_to_object(self.password_entry)
        self.pointing_device.click()

        #Intentionally cause passwords to mis-match
        self.keyboard.type('password')
        
        self.pointing_device.move_to_object(self.back_button)
        self.pointing_device.move_to_object(self.conf_pwd_entry)
        self.pointing_device.click()

        self.keyboard.type('will_not_match')
        
        #check that passwords match, and if not redo them
        self.check_passwords_match()

        self.pointing_device.move_to_object(self.continue_button)
        self.pointing_device.click()

    def check_passwords_match(self):

        while True:

            self.continue_button = self.app.select_single('GtkButton',
                                                          name='next')
            button_sensitive = self.continue_button.sensitive

            if button_sensitive == 1:
                self.assertThat(self.continue_button.sensitive, Equals(1))
                break

            #If passwords didn't match (which they didn't ;-) ) then retype them
            self.pointing_device.move_to_object(self.password_entry)
            self.pointing_device.click()
            self.keyboard.press_and_release('Ctrl+a')
            self.pointing_device.move_to_object(self.back_button)
            self.pointing_device.move_to_object(self.password_entry)
            self.keyboard.type('password')

            self.pointing_device.move_to_object(self.back_button)
            self.pointing_device.move_to_object(self.conf_pwd_entry)
            self.pointing_device.click()
            self.keyboard.press_and_release('Ctrl+a')
            self.pointing_device.move_to_object(self.back_button)
            self.pointing_device.move_to_object(self.password_entry)
            self.keyboard.type('password')

    def ubiquity_progress_bar_test(self):
        '''
            This method tracks the current progress of the install
        
            by using the fraction property of the progress bar
            
            to assertain the percentage complete.
                        
        '''
        #We cant assert page title here as its an external html page
        #Maybe try assert WebKitWebView is visible
        self.webkitwindow = self.app.select_single('GtkScrolledWindow',
                                                   name='webkit_scrolled_window')
        self.assertThat(self.webkitwindow.visible,
                        Eventually(Equals(1)))
        #Can we track the progress percentage?
        self.install_progress = self.app.select_single('GtkProgressBar',
                                                       name='install_progress')
                
        #Copying files progress bar
        self.track_install_progress_bar()
        
        self.assertThat(self.install_progress.fraction,
                        Eventually(Equals(0.0)))
        #And now the install progress bar
        self.track_install_progress_bar()
         
    def track_install_progress_bar(self):
        '''
            Gets the value of the fraction property of the progress bar
            
            so we can see when the progress bar is complete
            
        '''
        progress = 0.0
        complete = 1.0
        while progress < complete:
            #Lets check there have been no install errors while in this loop
            self.check_for_install_errors()
            #keep updating fraction value
            progress = self.install_progress.fraction
            # Use for debugging. Shows current 'fraction' value
            print(progress)

    def ubiquity_did_install_complete(self):
        self.complete_dialog = self.app.select_single('GtkDialog',
                                                      name='finished_dialog')
        self.assertThat(self.complete_dialog.title,
                        Eventually(Contains('Installation Complete')))
        self.con_testing_button = self.complete_dialog.select_single('GtkButton',
                                                                     name='quit_button')
        self.restart_button = self.complete_dialog.select_single('GtkButton',
                                                                 name='reboot_button')
        self.assertThat(self.complete_dialog.visible,
                        Eventually(Equals(1)))
        
    def wait_for_button_state_changed(self):
        '''
            This waits on the continuebutton becoming active again
        '''
        self.continue_button = self.app.select_single('GtkButton',
                                                      name='next')
        #check button disabled
        self.assertThat(self.continue_button.sensitive,
                        Eventually(Equals(0)))
        
        obj_prop = self.continue_button.sensitive
        #lets wait for button to enable again
        while obj_prop != 1:
            #keep grabbing the button to refresh it's state
            self.continue_button = self.app.select_single('GtkButton',
                                                          name='next')
            obj_prop = self.continue_button.sensitive

            #Check there are no errors while in this loop
            self.check_for_install_errors()
        #lets check it is enabled before returning
        self.assertThat(self.continue_button.sensitive,
                        Eventually(Equals(1)))

    def check_for_install_errors(self):
        '''
            This checks that no error/unwanted dialogs appear

            simply asserting that their visible properties = 0

            If they are not visible then there is no problems, UI wise that is! ;-)
        '''
        # For each dialog lets, select each dialog and finally check its not visible

        crash_dialog = self.app.select_single('GtkDialog',
                                              name='crash_dialog')
        self.assertThat(crash_dialog.visible,
                        Equals(0))

        warning_dialog = self.app.select_single('GtkDialog',
                                                name='warning_dialog')
        self.assertThat(warning_dialog.visible,
                        Equals(0))

    def get_ubiquity_objects(self):
        """ Selects all the objects needed for usage in the test """
    
        #-----------------------------------------------------------------------#
        #               OBJECTS THAT ARE ON EVERY PAGE                          #
        #                                                                       #
        self.headerlabel = self.app.select_single('GtkLabel', name='page_title')
        self.quit_button = self.app.select_single('GtkButton', name='quit')
        self.assertThat(self.quit_button.label, Equals('_Quit'))
        # We cannot assert continue button label here as the label value changes
        self.continue_button = self.app.select_single('GtkButton', name='next')
        #-----------------------------------------------------------------------#
        
        #-----------------------------------------------------------------------#
        #               OBJECTS THAT ARE ON MULTIPLE PAGES                      #
        #                                                                       #
        self.back_button = self.app.select_single('GtkButton', name='back')
        self.assertThat(self.back_button.label, Equals('_Back'))
        #-----------------------------------------------------------------------#
        
        #-----------------------------------------------------------------------#
        #            OBJECTS 'FROM PREPARING TO INSTALL' PAGE                   #
        #                                                                       #
        self.install_updates = self.app.select_single('GtkCheckButton',
                                                      name='prepare_download_updates')
        self.assertThat(self.install_updates.label,
                        Equals('Download updates while installing'))
        self.third_party = self.app.select_single('GtkCheckButton',
                                                  name='prepare_nonfree_software')
        self.assertThat(self.third_party.label,
                        Equals('Install this third-party software'))
        #------------------------------------------------------------------------#
        
        #------------------------------------------------------------------------#
        #            OBJECTS FROM THE 'INSTALLATION TYPE' PAGE                   #
        #                                                                        #
        self.erase_disk = self.app.select_single('GtkRadioButton',
                                                     name='use_device')    
        self.encrypt_install = self.app.select_single('GtkCheckButton',
                                                      name='use_crypto')
        self.assertThat(self.encrypt_install.label,
                        Equals('Encrypt the new Ubuntu installation for security'))
        self.lvm_install = self.app.select_single('GtkCheckButton',
                                                  name='use_lvm')
        self.assertThat(self.lvm_install.label,
                        Equals('Use LVM with the new Ubuntu installation'))
        self.something_else_install = self.app.select_single('GtkRadioButton',
                                                             name='custom_partitioning')
        self.assertThat(self.something_else_install.label,
                        Equals('Something else'))
        #-------------------------------------------------------------------------#
        
        #-------------------------------------------------------------------------#
        #            OBJECTS FROM THE KEYBOARD LAYOUT PAGE                        #
        #                                                                         #
        
        self.keyboard_entry = self.app.select_single('GtkEntry',
                                                     name='keyboard_test')
        self.keyboard_layout = self.app.select_single('GtkButton',
                                                      name='deduce_layout')
        self.assertThat(self.keyboard_layout.label,
                        Equals('Detect Keyboard Layout'))
        #-------------------------------------------------------------------------#
        
        #-------------------------------------------------------------------------#
        #             OBJECTS FROM THE 'WHO ARE YOU' PAGE                         #
        #                                                                         #
        self.user_gtkbox = self.app.select_single('GtkBox',
                                                  name='stepUserInfo')
        self.user_gtkgrid = self.user_gtkbox.select_single('GtkGrid',
                                                           name='userinfo_table')
        self.user_hbox1 = self.user_gtkgrid.select_single('GtkBox',
                                                          name='hbox1')
        self.password_entry = self.user_hbox1.select_single('GtkEntry',
                                                            name='password')
        self.user_hbox2 = self.user_gtkgrid.select_single('GtkBox',
                                                          name='hbox2')
        self.conf_pwd_entry = self.user_hbox2.select_single('GtkEntry',
                                                            name='verified_password')
        #--------------------------------------------------------------------------#
        
        #--------------------------------------------------------------------------#
        #              OBJECTS FROM LVM ENCRYPTION PASSWORD PAGE                       #
        #                                                                          #
        self.password_grid = self.app.select_single('GtkGrid', name='password_grid')
        self.encrypt_password = self.password_grid.select_single('GtkEntry',
                                                                 name='password')
        self.verify_encrypt_password = self.password_grid.select_single('GtkEntry',
                                                                        name='verified_password')
