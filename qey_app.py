"""
QEY Glyph Generator - Interactive GUI Application

A graphical application for creating, viewing, and exporting QEY glyphs.
This provides a user-friendly interface to the QEY glyph language system.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import io
import os
import json
import random
import threading

from qey_core import (
    QEYGlyph, QEYClass, QEYGenerator, AuthorityType, Capability,
    GlyphForm, PrimitiveElement, LayerType, generate_sample_glyphs
)
from qey_renderer import QEYRenderer, QEYAnimator


# =============================================================================
# MAIN APPLICATION
# =============================================================================

class QEYApp:
    """Main application class for the QEY Glyph Generator."""
    
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("QEY Glyph Generator - Darkbrane Protocol")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        
        # Set window icon if available
        try:
            self.root.iconbitmap(default='qey_icon.ico')
        except:
            pass
        
        # Initialize state
        self.current_glyph = None
        self.generator = QEYGenerator(seed=None)
        self.renderer = QEYRenderer(size=512, background_color=(0, 0, 0, 0))
        self.glyph_history = []
        self.current_history_index = -1
        
        # Create UI
        self._create_ui()
        
        # Generate a default glyph
        self._generate_default_glyph()
    
    def _create_ui(self):
        """Create the user interface."""
        # Main container
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_frame, bg='#16213e', width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Right panel - Glyph display
        right_panel = tk.Frame(main_frame, bg='#1a1a2e')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create control panels
        self._create_identity_panel(left_panel)
        self._create_authority_panel(left_panel)
        self._create_capabilities_panel(left_panel)
        self._create_actions_panel(left_panel)
        
        # Create display area
        self._create_display_area(right_panel)
        
        # Create status bar
        self._create_status_bar(main_frame)
    
    def _create_identity_panel(self, parent):
        """Create the identity configuration panel."""
        panel = tk.LabelFrame(
            parent,
            text=" Identity Configuration ",
            bg='#16213e',
            fg='#e94560',
            font=('Segoe UI', 10, 'bold')
        )
        panel.pack(fill=tk.X, pady=(10, 5), padx=5)
        
        # Identity data
        tk.Label(
            panel,
            text="Identity Data:",
            bg='#16213e',
            fg='#ffffff'
        ).pack(anchor=tk.W, pady=(5, 2), padx=5)
        
        self.identity_data_entry = tk.Entry(
            panel,
            bg='#0f3460',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief=tk.FLAT
        )
        self.identity_data_entry.pack(fill=tk.X, pady=(0, 5), padx=5)
        self.identity_data_entry.insert(0, "mateus_fiel_001")
        
        # QEY Class
        tk.Label(
            panel,
            text="QEY Class:",
            bg='#16213e',
            fg='#ffffff'
        ).pack(anchor=tk.W, pady=(5, 2), padx=5)
        
        self.qey_class_var = tk.StringVar(value="HUMAN")
        class_combobox = ttk.Combobox(
            panel,
            textvariable=self.qey_class_var,
            values=[c.name for c in QEYClass],
            state='readonly',
            style='Dark.TCombobox'
        )
        class_combobox.pack(fill=tk.X, pady=(0, 5), padx=5)
        
        # Glyph Form
        tk.Label(
            panel,
            text="Glyph Form:",
            bg='#16213e',
            fg='#ffffff'
        ).pack(anchor=tk.W, pady=(5, 2), padx=5)
        
        self.form_var = tk.StringVar(value="STATIC")
        form_combobox = ttk.Combobox(
            panel,
            textvariable=self.form_var,
            values=[f.name for f in GlyphForm],
            state='readonly',
            style='Dark.TCombobox'
        )
        form_combobox.pack(fill=tk.X, pady=(0, 5), padx=5)
        
        # Random seed
        tk.Label(
            panel,
            text="Random Seed:",
            bg='#16213e',
            fg='#ffffff'
        ).pack(anchor=tk.W, pady=(5, 2), padx=5)
        
        self.seed_entry = tk.Entry(
            panel,
            bg='#0f3460',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief=tk.FLAT
        )
        self.seed_entry.pack(fill=tk.X, pady=(0, 5), padx=5)
        self.seed_entry.insert(0, "42")
    
    def _create_authority_panel(self, parent):
        """Create the authority configuration panel."""
        panel = tk.LabelFrame(
            parent,
            text=" Authority Configuration ",
            bg='#16213e',
            fg='#e94560',
            font=('Segoe UI', 10, 'bold')
        )
        panel.pack(fill=tk.X, pady=(5, 5), padx=5)
        
        # Authority Type
        tk.Label(
            panel,
            text="Authority Type:",
            bg='#16213e',
            fg='#ffffff'
        ).pack(anchor=tk.W, pady=(5, 2), padx=5)
        
        self.authority_var = tk.StringVar(value="PERSONAL")
        authority_combobox = ttk.Combobox(
            panel,
            textvariable=self.authority_var,
            values=[a.name for a in AuthorityType],
            state='readonly',
            style='Dark.TCombobox'
        )
        authority_combobox.pack(fill=tk.X, pady=(0, 5), padx=5)
        
        # Authentication state (for Living glyphs)
        tk.Label(
            panel,
            text="Authenticated:",
            bg='#16213e',
            fg='#ffffff'
        ).pack(anchor=tk.W, pady=(5, 2), padx=5)
        
        self.authenticated_var = tk.BooleanVar(value=False)
        auth_check = tk.Checkbutton(
            panel,
            variable=self.authenticated_var,
            bg='#16213e',
            fg='#ffffff',
            selectcolor='#16213e',
            activebackground='#16213e',
            activeforeground='#ffffff'
        )
        auth_check.pack(anchor=tk.W, pady=(0, 5), padx=5)
        
        # Authentication phase slider
        tk.Label(
            panel,
            text="Auth Phase:",
            bg='#16213e',
            fg='#ffffff'
        ).pack(anchor=tk.W, pady=(5, 2), padx=5)
        
        self.auth_phase_var = tk.DoubleVar(value=0.0)
        auth_slider = tk.Scale(
            panel,
            from_=0,
            to=1,
            orient=tk.HORIZONTAL,
            variable=self.auth_phase_var,
            bg='#0f3460',
            fg='#ffffff',
            troughcolor='#0a1a2a',
            highlightbackground='#16213e'
        )
        auth_slider.pack(fill=tk.X, pady=(0, 5), padx=5)
    
    def _create_capabilities_panel(self, parent):
        """Create the capabilities configuration panel."""
        panel = tk.LabelFrame(
            parent,
            text=" Capabilities ",
            bg='#16213e',
            fg='#e94560',
            font=('Segoe UI', 10, 'bold')
        )
        panel.pack(fill=tk.X, pady=(5, 5), padx=5)
        
        # Capability checkboxes
        self.capability_vars = {}
        for i, capability in enumerate(Capability):
            var = tk.BooleanVar(value=False)
            self.capability_vars[capability.name] = var
            
            cb = tk.Checkbutton(
                panel,
                text=capability.name.replace('_', ' ').title(),
                variable=var,
                bg='#16213e',
                fg='#ffffff',
                selectcolor='#16213e',
                activebackground='#16213e',
                activeforeground='#ffffff',
                anchor=tk.W
            )
            cb.pack(fill=tk.X, pady=2, padx=5)
    
    def _create_actions_panel(self, parent):
        """Create the actions panel."""
        panel = tk.LabelFrame(
            parent,
            text=" Actions ",
            bg='#16213e',
            fg='#e94560',
            font=('Segoe UI', 10, 'bold')
        )
        panel.pack(fill=tk.X, pady=(5, 10), padx=5)
        
        # Generate button
        generate_btn = tk.Button(
            panel,
            text="Generate Glyph",
            command=self._generate_glyph,
            bg='#e94560',
            fg='#ffffff',
            activebackground='#c81e45',
            activeforeground='#ffffff',
            relief=tk.FLAT,
            font=('Segoe UI', 10, 'bold')
        )
        generate_btn.pack(fill=tk.X, pady=(5, 5), padx=5)
        
        # Export buttons
        export_frame = tk.Frame(panel, bg='#16213e')
        export_frame.pack(fill=tk.X, pady=(5, 5))
        
        export_png_btn = tk.Button(
            export_frame,
            text="Export PNG",
            command=self._export_png,
            bg='#0f3460',
            fg='#ffffff',
            activebackground='#0a1a2a',
            activeforeground='#ffffff',
            relief=tk.FLAT,
            font=('Segoe UI', 9)
        )
        export_png_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 2))
        
        export_json_btn = tk.Button(
            export_frame,
            text="Export JSON",
            command=self._export_json,
            bg='#0f3460',
            fg='#ffffff',
            activebackground='#0a1a2a',
            activeforeground='#ffffff',
            relief=tk.FLAT,
            font=('Segoe UI', 9)
        )
        export_json_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 5))
        
        # Animation buttons
        anim_frame = tk.Frame(panel, bg='#16213e')
        anim_frame.pack(fill=tk.X, pady=(5, 5))
        
        anim_auth_btn = tk.Button(
            anim_frame,
            text="Auth Animation",
            command=self._create_auth_animation,
            bg='#0f3460',
            fg='#ffffff',
            activebackground='#0a1a2a',
            activeforeground='#ffffff',
            relief=tk.FLAT,
            font=('Segoe UI', 9)
        )
        anim_auth_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 2))
        
        anim_pulse_btn = tk.Button(
            anim_frame,
            text="Pulse Animation",
            command=self._create_pulse_animation,
            bg='#0f3460',
            fg='#ffffff',
            activebackground='#0a1a2a',
            activeforeground='#ffffff',
            relief=tk.FLAT,
            font=('Segoe UI', 9)
        )
        anim_pulse_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 5))
        
        # Sample glyphs button
        samples_btn = tk.Button(
            panel,
            text="Load Sample Glyphs",
            command=self._load_sample_glyphs,
            bg='#0f3460',
            fg='#ffffff',
            activebackground='#0a1a2a',
            activeforeground='#ffffff',
            relief=tk.FLAT,
            font=('Segoe UI', 9)
        )
        samples_btn.pack(fill=tk.X, pady=(5, 5), padx=5)
    
    def _create_display_area(self, parent):
        """Create the glyph display area."""
        # Display frame
        display_frame = tk.Frame(parent, bg='#1a1a2e')
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Glyph canvas
        self.glyph_canvas = tk.Canvas(
            display_frame,
            bg='#1a1a2e',
            highlightthickness=0
        )
        self.glyph_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Glyph image label
        self.glyph_image_tk = None
        self.glyph_image_label = tk.Label(
            self.glyph_canvas,
            bg='#1a1a2e',
            highlightthickness=0
        )
        
        # Info display
        self.info_text = tk.Text(
            display_frame,
            height=8,
            bg='#0f3460',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief=tk.FLAT,
            font=('Consolas', 10)
        )
        self.info_text.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Bind mouse wheel for zooming
        self.glyph_canvas.bind("<MouseWheel>", self._on_mouse_wheel)
    
    def _create_status_bar(self, parent):
        """Create the status bar."""
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            parent,
            textvariable=self.status_var,
            bg='#0f3460',
            fg='#ffffff',
            anchor=tk.W,
            relief=tk.FLAT,
            font=('Segoe UI', 9)
        )
        status_bar.pack(fill=tk.X, pady=(5, 0))
    
    def _generate_default_glyph(self):
        """Generate a default glyph on startup."""
        self._generate_glyph()
    
    def _generate_glyph(self):
        """Generate a new glyph based on current settings."""
        try:
            # Get settings
            identity_data = self.identity_data_entry.get() or "default_identity"
            qey_class = QEYClass[self.qey_class_var.get()]
            authority_type = AuthorityType[self.authority_var.get()]
            form = GlyphForm[self.form_var.get()]
            seed_str = self.seed_entry.get()
            
            # Set seed
            seed = None
            if seed_str.strip():
                try:
                    seed = int(seed_str)
                except ValueError:
                    seed = hash(seed_str) % 1000000
            
            self.generator = QEYGenerator(seed=seed)
            
            # Get capabilities
            capabilities = []
            for cap_name, var in self.capability_vars.items():
                if var.get():
                    capabilities.append(Capability[cap_name])
            
            # Generate glyph
            self.current_glyph = self.generator.generate_glyph(
                identity_data=identity_data,
                qey_class=qey_class,
                authority_type=authority_type,
                capabilities=capabilities,
                form=form
            )
            
            # Set authentication state
            self.current_glyph.is_authenticated = self.authenticated_var.get()
            self.current_glyph.authentication_phase = self.auth_phase_var.get()
            
            # Render and display
            self._display_glyph()
            
            # Update info
            self._update_info()
            
            # Update status
            self.status_var.set(f"Generated {qey_class.name} glyph")
            
            # Save to history
            self._save_to_history()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate glyph: {e}")
    
    def _display_glyph(self):
        """Display the current glyph on the canvas."""
        if self.current_glyph is None:
            return
        
        # Clear previous image
        if self.glyph_image_tk:
            self.glyph_image_label.config(image=None)
            self.glyph_image_tk = None
        
        # Render glyph
        image = self.renderer.render_glyph(self.current_glyph, scale=1.0)
        
        # Resize for display
        display_size = min(self.glyph_canvas.winfo_width() or 500, 
                          self.glyph_canvas.winfo_height() or 500) - 40
        image = image.resize((display_size, display_size), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        self.glyph_image_tk = ImageTk.PhotoImage(image)
        
        # Update label
        self.glyph_image_label.config(image=self.glyph_image_tk)
        self.glyph_image_label.image = self.glyph_image_tk  # Keep reference
        
        # Place label in center
        self.glyph_image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def _update_info(self):
        """Update the info display with glyph details."""
        if self.current_glyph is None:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, "No glyph generated")
            return
        
        glyph = self.current_glyph
        
        info = f"QEY Glyph Information\n"
        info += f"======================\n"
        info += f"Identity Hash: {glyph.identity_hash}\n"
        info += f"Class: {glyph.qey_class.name}\n"
        info += f"Form: {glyph.form.name}\n"
        info += f"Authority: {glyph.authority_type.name}\n"
        info += f"Authenticated: {glyph.is_authenticated}\n"
        info += f"Auth Phase: {glyph.authentication_phase:.2f}\n"
        info += f"Capabilities: {', '.join(c.name for c in glyph.capabilities)}\n"
        info += f"Layers: {len(glyph.layers)}\n"
        
        # Count primitives
        total_primitives = sum(len(layer.primitives) for layer in glyph.layers.values())
        info += f"Total Primitives: {total_primitives}\n"
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info)
        self.info_text.config(state=tk.DISABLED)
    
    def _save_to_history(self):
        """Save the current glyph to history."""
        if self.current_glyph is None:
            return
        
        # Convert to dict for storage
        glyph_dict = self.current_glyph.to_dict()
        
        # Truncate history if too long
        if len(self.glyph_history) > 20:
            self.glyph_history = self.glyph_history[-19:]
            self.current_history_index -= 1
        
        # Add to history
        self.glyph_history.append(glyph_dict)
        self.current_history_index = len(self.glyph_history) - 1
    
    def _on_mouse_wheel(self, event):
        """Handle mouse wheel for zooming."""
        # This would require more complex implementation
        # For now, just regenerate the display
        self._display_glyph()
    
    def _export_png(self):
        """Export the current glyph as PNG."""
        if self.current_glyph is None:
            messagebox.showwarning("Warning", "No glyph to export")
            return
        
        # Ask for filename
        filename = filedialog.asksaveasfilename(
            defaultextension='.png',
            filetypes=[('PNG Image', '*.png'), ('All Files', '*.*')],
            title='Export PNG'
        )
        
        if filename:
            try:
                self.renderer.render_to_file(
                    self.current_glyph,
                    filename,
                    format='PNG'
                )
                self.status_var.set(f"Exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")
    
    def _export_json(self):
        """Export the current glyph as JSON."""
        if self.current_glyph is None:
            messagebox.showwarning("Warning", "No glyph to export")
            return
        
        # Ask for filename
        filename = filedialog.asksaveasfilename(
            defaultextension='.json',
            filetypes=[('JSON File', '*.json'), ('All Files', '*.*')],
            title='Export JSON'
        )
        
        if filename:
            try:
                glyph_dict = self.current_glyph.to_dict()
                
                with open(filename, 'w') as f:
                    json.dump(glyph_dict, f, indent=2)
                
                self.status_var.set(f"Exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")
    
    def _create_auth_animation(self):
        """Create an authentication animation GIF."""
        if self.current_glyph is None:
            messagebox.showwarning("Warning", "No glyph to animate")
            return
        
        # Ask for filename
        filename = filedialog.asksaveasfilename(
            defaultextension='.gif',
            filetypes=[('GIF Animation', '*.gif'), ('All Files', '*.*')],
            title='Export Authentication Animation'
        )
        
        if filename:
            try:
                # Create animator
                animator = QEYAnimator(
                    size=self.current_glyph.size,
                    fps=30,
                    duration=3.0,
                    background_color=(0, 0, 0, 0)
                )
                
                # Create animation in a thread to avoid freezing UI
                def create_animation():
                    try:
                        animator.create_authentication_animation(
                            self.current_glyph,
                            filename,
                            num_frames=60
                        )
                        self.root.after(0, lambda: self.status_var.set(f"Animation saved to {filename}"))
                    except Exception as e:
                        self.root.after(0, lambda: messagebox.showerror("Error", f"Animation failed: {e}"))
                
                thread = threading.Thread(target=create_animation, daemon=True)
                thread.start()
                
                self.status_var.set("Creating authentication animation...")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create animation: {e}")
    
    def _create_pulse_animation(self):
        """Create a pulse animation GIF."""
        if self.current_glyph is None:
            messagebox.showwarning("Warning", "No glyph to animate")
            return
        
        # Ask for filename
        filename = filedialog.asksaveasfilename(
            defaultextension='.gif',
            filetypes=[('GIF Animation', '*.gif'), ('All Files', '*.*')],
            title='Export Pulse Animation'
        )
        
        if filename:
            try:
                # Create animator
                animator = QEYAnimator(
                    size=self.current_glyph.size,
                    fps=30,
                    duration=3.0,
                    background_color=(0, 0, 0, 0)
                )
                
                # Create animation in a thread
                def create_animation():
                    try:
                        animator.create_pulse_animation(
                            self.current_glyph,
                            filename,
                            num_frames=60
                        )
                        self.root.after(0, lambda: self.status_var.set(f"Animation saved to {filename}"))
                    except Exception as e:
                        self.root.after(0, lambda: messagebox.showerror("Error", f"Animation failed: {e}"))
                
                thread = threading.Thread(target=create_animation, daemon=True)
                thread.start()
                
                self.status_var.set("Creating pulse animation...")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create animation: {e}")
    
    def _load_sample_glyphs(self):
        """Load sample glyphs for demonstration."""
        # Generate sample glyphs
        sample_glyphs = generate_sample_glyphs()
        
        # Create a simple dialog to select a sample
        sample_names = [
            f"{g.qey_class.name} - {g.form.name}" 
            for g in sample_glyphs
        ]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Sample Glyph")
        dialog.geometry("300x400")
        dialog.configure(bg='#16213e')
        
        tk.Label(
            dialog,
            text="Choose a sample glyph:",
            bg='#16213e',
            fg='#ffffff',
            font=('Segoe UI', 10, 'bold')
        ).pack(pady=10)
        
        listbox = tk.Listbox(
            dialog,
            bg='#0f3460',
            fg='#ffffff',
            selectbackground='#e94560',
            selectforeground='#ffffff',
            relief=tk.FLAT,
            font=('Segoe UI', 9)
        )
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for name in sample_names:
            listbox.insert(tk.END, name)
        
        def on_select():
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                self.current_glyph = sample_glyphs[index]
                self._display_glyph()
                self._update_info()
                self.status_var.set(f"Loaded sample: {sample_names[index]}")
                dialog.destroy()
        
        listbox.bind('<<ListboxSelect>>', lambda e: on_select())
        
        tk.Button(
            dialog,
            text="Close",
            command=dialog.destroy,
            bg='#e94560',
            fg='#ffffff',
            activebackground='#c81e45',
            activeforeground='#ffffff',
            relief=tk.FLAT
        ).pack(pady=10)


# =============================================================================
# STYLE CONFIGURATION
# =============================================================================

def configure_styles(root):
    """Configure custom styles for the application."""
    style = ttk.Style(root)
    
    # Configure dark theme
    style.theme_use('clam')
    
    # Frame style
    style.configure('TFrame', background='#16213e')
    
    # Combobox style
    style.configure('Dark.TCombobox', foreground='#ffffff', background='#0f3460')
    
    # Label style
    style.configure('TLabel', foreground='#ffffff', background='#16213e')


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main entry point for the application."""
    root = tk.Tk()
    
    # Configure styles
    configure_styles(root)
    
    # Create application
    app = QEYApp(root)
    
    # Run main loop
    root.mainloop()


if __name__ == "__main__":
    main()
